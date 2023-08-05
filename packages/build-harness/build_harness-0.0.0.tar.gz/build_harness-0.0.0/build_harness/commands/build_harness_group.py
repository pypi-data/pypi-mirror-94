#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""CLI command processing for ``build-harness`` command."""

import pathlib
import sys

import click

from build_harness._version import acquire_version

from .analysis import static_analysis
from .bdd import bdd_acceptance_command
from .bootstrap import install
from .code_style import formatting
from .publishing import publish
from .state import CommandState
from .unit_tests import unit_test
from .wheel import package

DEFAULT_PROJECT_PATH = "."


@click.group()
@click.pass_context
@click.version_option(version=acquire_version())
def main(ctx: click.Context) -> None:
    """Build harness group."""
    ctx.obj = CommandState(
        project_path=pathlib.Path(DEFAULT_PROJECT_PATH),
        venv_path=pathlib.Path(sys.argv[0]).parent.absolute(),
    )


main.add_command(bdd_acceptance_command, name="acceptance")
main.add_command(formatting, name="formatting")
main.add_command(install, name="install")
main.add_command(package, name="package")
main.add_command(publish, name="publish")
main.add_command(static_analysis, name="static-analysis")
main.add_command(unit_test, name="unit-test")
