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
import subprocess

import pytest
from setup_scmversion.util import execute_command


def test_execute_command_ok():
    assert execute_command('echo something') == ('something\n', '')


def test_execute_command_error():
    with pytest.raises(subprocess.CalledProcessError):
        assert execute_command('arisetnrasitn') == ''


def test_execute_command_stderr():
    assert execute_command('echo "this will go to stderr" > /dev/stderr') == \
        ('', "this will go to stderr\n")
