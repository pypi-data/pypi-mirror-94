#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""
CLI argument and command processing.

Exports:

*  ``ExitState`` class
*  ``main`` function
"""

from .build_harness_group import main  # noqa: F401
from .state import ExitState  # noqa: F401
