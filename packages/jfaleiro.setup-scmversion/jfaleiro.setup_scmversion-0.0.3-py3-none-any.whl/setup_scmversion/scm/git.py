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

import logging
from functools import lru_cache
from typing import Tuple

from ..parser import ScmParser, Tags
from ..util import execute_command


class GitError(Exception):
    pass


class GitParser(ScmParser):

    def __init__(self, executor=execute_command):
        self.executor = executor

    def _git_command(self, command: str) -> str:
        out, err = self.executor(command)
        def flatten(x): return ''.join(x.split('\n'))
        flatten_out, flatten_err = flatten(out), flatten(err)
        if len(flatten_err) > 0:
            raise GitError(command, err, out)
        return flatten_out

    @property
    @lru_cache()
    def branch(self):
        return self._git_command('git rev-parse --abbrev-ref HEAD')

    @property
    @lru_cache()
    def commits(self):
        return self._git_command(f'git rev-list --count {self.branch}')

    @property
    @lru_cache()
    def tag(self):
        try:
            tag = self._git_command('git describe --tags')
            # check for tag out of the ordinary, i.e.
            # fatal: No names found, cannot describe anything.
            if tag.startswith('fatal:'):
                logging.info(f'no previous tags: "{tag}"')
                tag = None
        except Exception:
            logging.exception('cannot describe tag, will use None')
            tag = None
        return tag

    @staticmethod
    def build_version(branch: str, commits: str, tag: str) -> Tuple[Tags, str]:
        if branch in ['master', 'HEAD']:
            if tag is None or len(tag.strip()) == 0:
                return Tags.OTHER, f'master.dev{commits}'
            else:
                # 0.0.2-1-g5c0bb91 or 0.0.2
                parts = tag.split('-')
                if len(parts) == 1:  # 0.0.2
                    return Tags.RELEASE, tag
                else:
                    return Tags.OTHER, tag
        elif branch.startswith('release/'):
            return (Tags.RELEASE_BRANCH,
                    branch.split('/')[-1] + f'.dev{commits}')
        elif branch.startswith('feature/'):
            return (Tags.FEATURE_BRANCH,
                    branch.split('/')[-1] + f'.feature{commits}')
        else:
            return (Tags.OTHER,
                    f'unversioned.dev{commits}')

    def version(self) -> str:
        """builds a version number based on information on the scm"""
        return GitParser.build_version(self.branch, self.commits, self.tag)[1]

    def version_type(self) -> Tags:
        """finds the version type based on information on the scm"""
        return GitParser.build_version(self.branch, self.commits, self.tag)[0]
