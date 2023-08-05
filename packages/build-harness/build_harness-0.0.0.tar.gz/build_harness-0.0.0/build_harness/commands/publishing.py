#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Package publish subcommand implementation."""

import copy
import logging
import pathlib
import sys

import click

from build_harness._utility import (
    CommandArgs,
    command_path,
    report_console_error,
    run_command,
)

from .state import CommandState, ExitState

log = logging.getLogger(__name__)

FLIT_PUBLISH_CMD: CommandArgs = ["flit", "publish"]


class PublishingError(Exception):
    """Problem occurred during publishing."""


def _publish_flit_package(venv_path: pathlib.Path) -> None:
    """
    Publish package using flit.

    Args:
        venv_path: Path to Python virtual environment.

    Raises:
        PublishingError: If package publish exits non-zero.
    """
    flit_cmd = copy.deepcopy(FLIT_PUBLISH_CMD)
    flit_cmd[0] = command_path(venv_path, flit_cmd)
    result = run_command(flit_cmd)

    if any([x != 0 for x in [result.returncode]]):
        raise PublishingError("flit failed during package publishing.")


@click.command()
@click.pass_context
def publish(ctx: click.Context) -> None:
    """Publish project artifacts."""
    try:
        command_state: CommandState = ctx.obj

        _publish_flit_package(command_state.venv_path)
    except PublishingError as e:
        message = str(e)
        log.exception(message)
        report_console_error(message)
        sys.exit(ExitState.PUBLISHING_FAILED)
    except Exception:
        message = "Unexpected error. Check log for details."
        log.exception(message)
        report_console_error(message)
        sys.exit(ExitState.UNKNOWN_ERROR)
