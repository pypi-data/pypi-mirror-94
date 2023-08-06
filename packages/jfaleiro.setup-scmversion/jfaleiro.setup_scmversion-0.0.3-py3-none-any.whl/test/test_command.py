#
#     setup_scmversion - Builds a pythonic version number based on scm tags
#                        and branches.
#
#     Copyright (C) 2019 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from setuptools import Distribution

import pytest
from setup_scmversion.command import TagVersionCommand
from setup_scmversion.parser import DEFAULT_SCM


@pytest.fixture
def distribution():
    return Distribution()


@pytest.fixture
def command(distribution):
    return TagVersionCommand(distribution)


def test_instantiation(command):
    command.initialize_options()
    assert command.package is None
    assert command.file is None
    assert command.scm == DEFAULT_SCM
    command.finalize_options()


def test_run(command, capsys):
    command.initialize_options()
    command.finalize_options()
    command.run()
    captured = capsys.readouterr()
    p = captured.out
    assert p == "tagged ('setup_scmversion', '_version.py')\n"
