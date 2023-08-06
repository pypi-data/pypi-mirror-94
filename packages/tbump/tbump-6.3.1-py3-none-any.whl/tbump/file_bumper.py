import glob
import re
from pathlib import Path
from typing import Dict, List, Optional, Pattern

import attr
import cli_ui as ui

import tbump
import tbump.action
import tbump.config
import tbump.git


@attr.s
class ChangeRequest:
    src: str = attr.ib()
    old_string: str = attr.ib()
    new_string: str = attr.ib()
    search: Optional[str] = attr.ib(default=None)


class Patch(tbump.action.Action):
    def __init__(
        self, working_path: Path, src: str, lineno: int, old_line: str, new_line: str
    ):
        super().__init__()
        self.working_path = working_path
        self.src = src
        self.lineno = lineno
        self.old_line = old_line
        self.new_line = new_line

    def print_self(self) -> None:
        # fmt: off
        ui.info(
            ui.red, "- ", ui.reset,
            ui.bold, self.src, ":", ui.reset,
            ui.darkgray, self.lineno + 1, ui.reset,
            " ", ui.red, self.old_line.strip(),
            sep="",
        )
        ui.info(
            ui.green, "+ ", ui.reset,
            ui.bold, self.src, ":", ui.reset,
            ui.darkgray, self.lineno + 1, ui.reset,
            " ", ui.green, self.new_line.strip(),
            sep="",
        )
        # fmt: on

    def do(self) -> None:
        self.apply()

    @staticmethod
    def get_ending(line: bytes) -> bytes:
        if line.endswith(b"\r\n"):
            return b"\r\n"
        else:
            return b"\n"

    def apply(self) -> None:
        file_path = self.working_path / self.src
        contents = file_path.read_bytes()
        lines = contents.splitlines(keepends=True)
        old_line = lines[self.lineno]
        lines[self.lineno] = self.new_line.encode() + Patch.get_ending(old_line)
        text = b"".join(lines)
        file_path.write_bytes(text)


class BadSubstitution(tbump.Error):
    def __init__(
        self,
        *,
        src: str,
        verb: str,
        groups: Dict[str, str],
        template: str,
        version: str
    ):
        super().__init__()
        self.src = src
        self.verb = verb
        self.groups = groups
        self.template = template
        self.version = version

    def print_error(self) -> None:
        message = [
            " ",
            self.src + ":",
            " refusing to ",
            self.verb,
            " version containing 'None'\n",
        ]
        message += [
            "More info:\n",
            " * version groups:  ",
            repr(self.groups),
            "\n" " * template:        ",
            self.template,
            "\n",
            " * version:         ",
            self.version,
            "\n",
        ]
        ui.error(*message, end="", sep="")


class InvalidVersion(tbump.Error):
    def __init__(self, *, version: str, regex: Pattern[str]):
        super().__init__()
        self.version = version
        self.regex = regex

    def print_error(self) -> None:
        ui.error("Could not parse", self.version, "as a valid version string")


class SourceFileNotFound(tbump.Error):
    def __init__(self, *, src: str):
        super().__init__()
        self.src = src

    def print_error(self) -> None:
        ui.error(self.src, "does not exist")


class CurrentVersionNotFound(tbump.Error):
    def __init__(self, *, src: str, current_version_string: str):
        super().__init__()
        self.src = src
        self.current_version_string = current_version_string

    # TODO: raise just once for all errors
    def print_error(self) -> None:
        ui.error(
            "Current version string: (%s)" % self.current_version_string,
            "not found in",
            self.src,
        )


def should_replace(line: str, old_string: str, search: Optional[str] = None) -> bool:
    if not search:
        return old_string in line
    else:
        return (old_string in line) and (re.search(search, line) is not None)


def on_version_containing_none(
    src: str, verb: str, version: str, *, groups: Dict[str, str], template: str
) -> None:
    raise BadSubstitution(
        src=src, verb=verb, version=version, groups=groups, template=template
    )


class FileBumper:
    def __init__(self, working_path: Path):
        self.working_path = working_path
        self.files: List[tbump.config.File] = []
        self.version_regex = re.compile(".")
        self.current_version = ""
        self.current_groups: Dict[str, str] = {}
        self.new_version = ""
        self.new_groups: Dict[str, str] = {}
        self.config_file: Optional[tbump.config.ConfigFile] = None

    def parse_version(self, version: str) -> Dict[str, str]:
        assert self.version_regex
        match = self.version_regex.fullmatch(version)
        if match is None:
            raise InvalidVersion(version=version, regex=self.version_regex)
        return match.groupdict()

    def set_config_file(self, config_file: tbump.config.ConfigFile) -> None:
        self.config_file = config_file
        config = config_file.get_config()
        self.files = config.files
        self.check_files_exist()
        self.version_regex = config.version_regex
        self.current_version = config.current_version
        self.current_groups = self.parse_version(self.current_version)

    def check_files_exist(self) -> None:
        assert self.files
        for file in self.files:
            expected_path = self.working_path / file.src
            files_found = glob.glob(str(expected_path), recursive=True)
            if not files_found:
                raise SourceFileNotFound(src=file.src)

    def get_patches(self, new_version: str) -> List[Patch]:
        self.new_version = new_version
        self.new_groups = self.parse_version(self.new_version)
        change_requests = self.compute_change_requests()
        patches = []
        for change_request in change_requests:
            patches_for_request = self.compute_patches_for_change_request(
                change_request
            )
            patches.extend(patches_for_request)
        return patches

    def compute_patches_for_change_request(
        self, change_request: ChangeRequest
    ) -> List[Patch]:
        old_string = change_request.old_string
        new_string = change_request.new_string
        search = change_request.search
        patches = []

        file_path_glob = self.working_path / change_request.src
        for file_path_str in glob.glob(str(file_path_glob), recursive=True):
            file_path = Path(file_path_str)
            expanded_src = file_path.relative_to(self.working_path)
            old_lines = file_path.read_text().splitlines(keepends=False)

            for i, old_line in enumerate(old_lines):
                if should_replace(old_line, old_string, search):
                    new_line = old_line.replace(old_string, new_string)
                    patch = Patch(
                        self.working_path, str(expanded_src), i, old_line, new_line
                    )
                    patches.append(patch)
        if not patches:
            raise CurrentVersionNotFound(
                src=change_request.src, current_version_string=old_string
            )
        return patches

    def compute_change_requests(self) -> List[ChangeRequest]:
        # When bumping files in a project, we need to bump:
        #  * every file listed in the config file
        #  * and the `current_version` value in tbump's config file
        assert self.config_file
        change_requests = []
        for file in self.files:
            change_request = self.compute_change_request_for_file(file)
            change_requests.append(change_request)
        rel_path = self.config_file.path.relative_to(self.working_path)
        config_file_change = ChangeRequest(
            str(rel_path),
            self.current_version,
            self.new_version,
        )
        change_requests.append(config_file_change)
        return change_requests

    def compute_change_request_for_file(self, file: tbump.config.File) -> ChangeRequest:
        if file.version_template:
            current_version = file.version_template.format(**self.current_groups)
            if "None" in current_version:
                on_version_containing_none(
                    file.src,
                    "look for",
                    current_version,
                    groups=self.current_groups,
                    template=file.version_template,
                )
            new_version = file.version_template.format(**self.new_groups)
            if "None" in new_version:
                on_version_containing_none(
                    file.src,
                    "replace by",
                    new_version,
                    groups=self.new_groups,
                    template=file.version_template,
                )
        else:
            current_version = self.current_version
            new_version = self.new_version

        to_search = None
        if file.search:
            to_search = file.search.format(current_version=re.escape(current_version))

        return ChangeRequest(file.src, current_version, new_version, search=to_search)


def bump_files(new_version: str, repo_path: Optional[Path] = None) -> None:
    repo_path = repo_path or Path(".")
    bumper = FileBumper(repo_path)
    config_file = tbump.config.get_config_file(repo_path)
    bumper.set_config_file(config_file)
    patches = bumper.get_patches(new_version=new_version)
    n = len(patches)
    for i, patch in enumerate(patches):
        ui.info_count(i, n, patch.src)
        patch.print_self()
        patch.apply()
