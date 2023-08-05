#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import subprocess

import pytest

from build_harness.commands import main
from tests.ci.support.click_runner import click_runner  # noqa: F401


@pytest.fixture()
def mock_run(mock_sysargv, mocker):
    mock_pytest_result = mocker.create_autospec(subprocess.CompletedProcess)
    mock_pytest_result.returncode = 0
    mock_pytest_result.stdout = ""
    this_run = mocker.patch(
        "build_harness.commands.publishing.run_command",
        return_value=mock_pytest_result,
    )

    return this_run


class TestPublish:
    def test_default(self, click_runner, mocker, mock_run):
        result = click_runner.invoke(
            main,
            [
                "publish",
            ],
        )

        assert result.exit_code == 0
        mock_run.assert_has_calls(
            [
                mocker.call(
                    ["/some/path/flit", "publish"],
                ),
            ]
        )
