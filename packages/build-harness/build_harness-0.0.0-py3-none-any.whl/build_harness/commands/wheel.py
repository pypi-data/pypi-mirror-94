#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Package generation subcommand implementation."""

import copy
import logging
import pathlib
import sys
import typing

import click
import parver  # type: ignore

from build_harness._project import acquire_source_dir
from build_harness._utility import (
    CommandArgs,
    command_path,
    report_console_error,
    run_command,
)

from .state import CommandState, ExitState

log = logging.getLogger(__name__)

DEFAULT_VERSION_FILE = "VERSION"

FLIT_BUILD_CMD: CommandArgs = ["flit", "build"]


class PackagingError(Exception):
    """Problem occurred during packaging."""


class InvalidReleaseId(PackagingError):
    """Parsed release ID is not valid PEP-440."""


class ReleaseEmptyOption(click.Option):
    """Optional release id with empty value."""

    empty_value = True


T = typing.TypeVar("T", bound="ReleaseValueOption")


class ReleaseValueOption(click.Option):
    """Fix the help for the _set suffix."""

    def get_help_record(self: T, ctx: click.Context) -> typing.Tuple[str, str]:
        """Customize help text."""
        help = super(ReleaseValueOption, self).get_help_record(ctx)
        return (help[0].replace("_set ", " "),) + help[1:]


U = typing.TypeVar("U", bound="ReleaseIdCommand")


class ReleaseIdCommand(click.Command):
    """Custom release id parsing."""

    def parse_args(
        self: U, ctx: click.Context, args: typing.List[str]
    ) -> typing.List[str]:
        """Translate empty value to non-empty as needed."""
        for i, a in enumerate(args):
            # For this to be a non-empty release id there must be at least one more
            # argument.
            if (a == "--release-id") and ((len(args) - 2) >= i):
                # modify the argument to be a non-empty argument
                a += "_set"
                args[i] = a

        return super(ReleaseIdCommand, self).parse_args(ctx, args)


def _validate_release_id(release_id: str) -> None:
    """
    Validate release id according to PEP-440.

    https://www.python.org/dev/peps/pep-0440/

    Args:
        release_id: Release id to validate.

    Raises:
        InvalidReleaseId: If release id is not valid PEP-440.
    """
    try:
        parver.Version.parse(release_id)
    except parver.ParseError as e:
        raise InvalidReleaseId(str(e)) from e


def _apply_release_id(release_id: str, version_file_path: pathlib.Path) -> None:
    """
    Apply the release id to the project source package directory.

    Args:
        release_id: Release id to be applied to source directory.
        project_path: Path to project directory.
    """
    _validate_release_id(release_id)

    with version_file_path.open(mode="w") as f:
        f.write(release_id)


def _build_flit_package(venv_path: pathlib.Path) -> None:
    """
    Build packages using flit.

    Args:
        venv_path: Path to Python virtual environment.

    Raises:
        PackagingError: If package build exits non-zero.
    """
    flit_cmd = copy.deepcopy(FLIT_BUILD_CMD)
    flit_cmd[0] = command_path(venv_path, flit_cmd)
    result = run_command(flit_cmd)

    if any([x != 0 for x in [result.returncode]]):
        raise PackagingError("flit failed during package build.")


@click.command(cls=ReleaseIdCommand)
@click.pass_context
@click.option(
    "--release-id",
    cls=ReleaseEmptyOption,
    help="Apply default release id",
    is_flag=True,
)
@click.option(
    "--release-id_set",
    cls=ReleaseValueOption,
    default=None,
    help="PEP-440 release id to apply to package. [default: do nothing]",
    type=str,
)
def package(
    ctx: click.Context, release_id: bool, release_id_set: typing.Optional[str]
) -> None:
    """Build wheel, sdist packages."""
    try:
        command_state: CommandState = ctx.obj

        source_dir = pathlib.Path(acquire_source_dir(command_state.project_path))
        version_file_path = source_dir / DEFAULT_VERSION_FILE

        try:
            if release_id_set:
                _apply_release_id(release_id_set, version_file_path)

            _build_flit_package(command_state.venv_path)
        except PackagingError as e:
            message = str(e)
            log.error(message)
            report_console_error(message)
            sys.exit(ExitState.PACKAGING_FAILED)
        finally:
            version_file_path.unlink(missing_ok=True)
    except Exception:
        message = "Unexpected error. Check log for details."
        log.exception(message)
        report_console_error(message)
        sys.exit(ExitState.UNKNOWN_ERROR)
