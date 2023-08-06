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
from unittest.mock import MagicMock

import pytest
from setup_scmversion.parser import Tags
from setup_scmversion.scm.git import GitParser


@pytest.fixture
def parser():
    return GitParser()


def test_branch_mock():
    branch = 'release/0.0.1'
    parser = GitParser(executor=MagicMock(return_value=(branch + '\n', '')))
    assert parser.branch == branch


def test_branch(parser):
    branch = parser.branch
    assert isinstance(branch, str)
    assert len(branch) > 0


def test_commits_mock():
    commits = '23'
    parser = GitParser(executor=MagicMock(
        return_value=(str(commits) + '\n', '')))
    assert parser.commits == commits


def test_commits(parser):
    commits = parser.commits
    assert isinstance(commits, str)
    assert len(commits) > 0
    assert int(commits) > 0


def test_tag(parser):
    branch = parser.branch
    assert isinstance(branch, str)
    assert len(branch) > 0


def test_tag_message_no_tags_found():
    parser = GitParser(executor=MagicMock(
        return_value=('fatal: No names found, cannot describe anything.\n',
                       '')))
    assert parser.tag is None


def test_tag_raise_exception():
    parser = GitParser(executor=MagicMock(raises=Exception()))
    assert parser.tag is None


def test_tag_fatal_message():
    parser = GitParser(executor=MagicMock(
        return_value=('',
                       'git not installed.\n')))
    assert parser.tag is None


def test_build_version_release_branch():
    assert GitParser.build_version(
        'release/0.0.1', '12', None) == (Tags.RELEASE_BRANCH, '0.0.1.dev12')
    assert GitParser.build_version(
        'release/0.0.1', '12', '') == (Tags.RELEASE_BRANCH, '0.0.1.dev12')


def test_build_version_feature_branch():
    assert GitParser.build_version(
        'feature/0.0.1', '12', None) == (Tags.FEATURE_BRANCH,
                                         '0.0.1.feature12')
    assert GitParser.build_version(
        'feature/0.0.1', '12', '') == (Tags.FEATURE_BRANCH, '0.0.1.feature12')


def test_build_version_release():
    assert GitParser.build_version('master', '12', '0.0.1') == (
        Tags.RELEASE, '0.0.1')


def test_build_version_other():
    assert GitParser.build_version('master', '12', None) == (
        Tags.OTHER, 'master.dev12')
    assert GitParser.build_version('master', '12', '') == (
        Tags.OTHER, 'master.dev12')
    assert GitParser.build_version('master', '12', '0.0.1-1-g5c0bb91') == (
        Tags.OTHER, '0.0.1-1-g5c0bb91')
    assert GitParser.build_version('releases/0.0.1', '12',
                                   '0.0.1-1-g5c0bb91') == (
        Tags.OTHER,
        'unversioned.dev12')
