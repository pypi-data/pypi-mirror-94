import abc
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern

import attr
import cli_ui as ui
import schema
import tomlkit
from tomlkit.toml_document import TOMLDocument

import tbump

from .hooks import HOOKS_CLASSES, Hook


@attr.s
class File:
    src: str = attr.ib()
    search: Optional[str] = attr.ib(default=None)
    version_template: Optional[str] = attr.ib(default=None)


@attr.s
class Config:
    current_version: str = attr.ib()
    version_regex: Pattern[str] = attr.ib()

    git_tag_template: str = attr.ib()
    git_message_template: str = attr.ib()

    files: List[File] = attr.ib()
    hooks: List[Hook] = attr.ib()

    github_url: Optional[str] = attr.ib()


class ConfigFile(metaclass=abc.ABCMeta):
    """ Base class representing a config file """

    def __init__(self, path: Path):
        self.path = path

    @abc.abstractmethod
    def get_parsed(self) -> Any:
        """Return a plain dictionnary, suitable for validation
        by the `schema` library
        """
        pass

    def get_config(self) -> Config:
        """Return a validated Config instance"""
        parsed = self.get_parsed()
        res = from_parsed_config(parsed)
        validate_config(res)
        return res


class TbumpTomlConfig(ConfigFile):
    """Represent config inside a tbump.toml file"""

    def __init__(self, path: Path, doc: TOMLDocument):
        super().__init__(path)
        self.doc = doc

    def get_parsed(self) -> Any:
        return self.doc.value


class PyprojectConfig(ConfigFile):
    """Represent a config inside a pyproject.toml file,
    under the [tool.tbump] key
    """

    def __init__(self, path: Path, doc: TOMLDocument):
        self.doc = doc
        super().__init__(path)

    def get_parsed(self) -> Any:
        return self.doc["tool"]["tbump"].value


def validate_template(name: str, pattern: str, value: str) -> None:
    if pattern not in value:
        message = "%s should contain the string %s" % (name, pattern)
        raise schema.SchemaError(message)


def validate_git_tag_template(value: str) -> None:
    validate_template("git.tag_template", "{new_version}", value)


def validate_git_message_template(value: str) -> None:
    validate_template("git.message_template", "{new_version}", value)


def validate_version_template(
    src: str, version_template: str, known_groups: Dict[str, str]
) -> None:
    try:
        version_template.format(**known_groups)
    except KeyError as e:
        message = "version template for '%s' contains unknown group: %s" % (src, e)
        raise schema.SchemaError(message)


def validate_hook_cmd(cmd: str) -> None:
    try:
        cmd.format(new_version="dummy", current_version="dummy")
    except KeyError as e:
        message = "hook cmd: '%s' uses unknown placeholder: %s" % (cmd, e)
        raise schema.SchemaError(message)


def validate_basic_schema(config: Any) -> None:
    """ First pass of validation, using schema """
    # Note: asserts that we won't get KeyError or invalid types
    # when building or initial Config instance
    file_schema = schema.Schema(
        {
            "src": str,
            schema.Optional("search"): str,
            schema.Optional("version_template"): str,
        }
    )

    hook_schema = schema.Schema({"name": str, "cmd": str})

    def validate_re(regex: str) -> str:
        re.compile(regex, re.VERBOSE)
        return regex

    tbump_schema = schema.Schema(
        {
            "version": {"current": str, "regex": schema.Use(validate_re)},
            "git": {"message_template": str, "tag_template": str},
            "file": [file_schema],
            schema.Optional("hook"): [hook_schema],  # retro-compat
            schema.Optional("before_push"): [hook_schema],  # retro-compat
            schema.Optional("before_commit"): [hook_schema],
            schema.Optional("after_push"): [hook_schema],
            schema.Optional("github_url"): str,
        }
    )
    tbump_schema.validate(config)


def validate_config(cfg: Config) -> None:
    """Second pass of validation, using the Config
    class.

    """
    # Note: separated from validate_basic_schema to keep error
    # messages user friendly

    current_version = cfg.current_version

    validate_git_message_template(cfg.git_message_template)
    validate_git_tag_template(cfg.git_tag_template)

    match = cfg.version_regex.fullmatch(current_version)
    if not match:
        message = "Current version: %s does not match version regex" % current_version
        raise schema.SchemaError(message)
    current_version_regex_groups = match.groupdict()

    for file_config in cfg.files:
        version_template = file_config.version_template
        if version_template:
            validate_version_template(
                file_config.src, version_template, current_version_regex_groups
            )

    for hook in cfg.hooks:
        validate_hook_cmd(hook.cmd)


def get_config_file(project_path: Path) -> ConfigFile:
    try:
        res = _get_config_file(project_path)
        # Check that the config is valid before returning it,
        # so that problems in config file are reported early
        res.get_config()
        return res
    except IOError as io_error:
        raise InvalidConfig(io_error=io_error)
    except schema.SchemaError as parse_error:
        raise InvalidConfig(parse_error=parse_error)


def _get_config_file(project_path: Path) -> ConfigFile:
    toml_path = project_path / "tbump.toml"
    if toml_path.exists():
        doc = tomlkit.loads(toml_path.read_text())
        return TbumpTomlConfig(toml_path, doc)

    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        doc = tomlkit.loads(pyproject_path.read_text())
        try:
            doc["tool"]["tbump"]
        except KeyError:
            raise ConfigNotFound(project_path)
        return PyprojectConfig(pyproject_path, doc)

    raise ConfigNotFound(project_path)


def from_parsed_config(parsed: Any) -> Config:
    validate_basic_schema(parsed)
    current_version = parsed["version"]["current"]
    git_message_template = parsed["git"]["message_template"]
    git_tag_template = parsed["git"]["tag_template"]
    version_regex = re.compile(parsed["version"]["regex"], re.VERBOSE)
    files = []
    for file_dict in parsed["file"]:
        file_config = File(
            src=file_dict["src"],
            search=file_dict.get("search"),
            version_template=file_dict.get("version_template"),
        )
        files.append(file_config)

    hooks = []
    for hook_type in ("hook", "before_push", "before_commit", "after_push"):
        cls = HOOKS_CLASSES[hook_type]
        if hook_type in parsed:
            for hook_dict in parsed[hook_type]:
                hook = cls(hook_dict["name"], hook_dict["cmd"])
                hooks.append(hook)

    github_url = parsed.get("github_url")

    config = Config(
        current_version=current_version,
        version_regex=version_regex,
        git_message_template=git_message_template,
        git_tag_template=git_tag_template,
        files=files,
        hooks=hooks,
        github_url=github_url,
    )

    validate_config(config)

    return config


class ConfigNotFound(tbump.Error):
    def __init__(self, project_path: Path):
        self.project_path = project_path

    def print_error(self) -> None:
        ui.error("No configuration for tbump fond in", self.project_path)
        ui.info("Please run `tbump init` to create a tbump.toml file")
        ui.info("Or add a [tool.tbump] section in the pyproject.toml file")


class InvalidConfig(tbump.Error):
    def __init__(
        self,
        io_error: Optional[IOError] = None,
        parse_error: Optional[Exception] = None,
    ):
        super().__init__()
        self.io_error = io_error
        self.parse_error = parse_error

    def print_error(self) -> None:
        if self.io_error:
            ui.error("Could not read config file:", self.io_error)
        if self.parse_error:
            ui.error("Invalid config:", self.parse_error)
