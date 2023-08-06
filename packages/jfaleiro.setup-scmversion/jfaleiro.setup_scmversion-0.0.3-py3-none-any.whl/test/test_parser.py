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


import pytest
from setup_scmversion.parser import parser_factory, parsers, tag_version
from setup_scmversion.scm.git import GitParser


def test_parsers():
    assert parsers() == "['git']"


def test_parser_factory():
    parser = parser_factory(scm='git')
    assert parser == parser_factory(scm='git')


def test_parser_factory_default_is_git():
    parser = parser_factory()
    assert isinstance(parser, GitParser)


def test_parser_factory_invalid():
    with pytest.raises(ValueError) as e:
        parser_factory(scm='blah')
    assert e.value.args == ("scm 'blah' invalid (options: ['git'])",)


def test_tag_version():
    assert tag_version() == ('setup_scmversion', '_version.py')


def test_tag_version_no_packages_detected():
    with pytest.raises(ValueError) as e:
        tag_version(exclude='test setup_scmversion'.split())
    assert e.value.args == ('no default package detected',)


def test_tag_version_multiple_packages_detected():
    with pytest.raises(ValueError) as e:
        tag_version(exclude=[])
    assert e.value.args == (
        "multiple packages detected: ['setup_scmversion', 'test']",)
