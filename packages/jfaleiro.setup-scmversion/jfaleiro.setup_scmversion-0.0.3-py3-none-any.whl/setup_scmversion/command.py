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

import os
from distutils.cmd import Command

from .parser import DEFAULT_SCM, PARSERS, init, parser_factory, tag_version


class TagVersionCommand(Command):
    """
    Tags <package>/version.py with the version number
    """
    description = __doc__.strip()
    user_options = [
        ('package=', 'p',
            ('name of the main package where the '
             'version file will be overwritten')),
        ('file=', 'f', 'name of the file'),
        ('scm=', 's', 'key for the scm'),
    ]

    def initialize_options(self):
        self.package = None
        self.file = None
        self.scm = DEFAULT_SCM

    def finalize_options(self):
        init()
        assert self.package is None or os.path.exists(
            self.package), 'package does not exist: %s' % self.package
        assert self.scm in PARSERS.keys()

    def run(self):
        parser = parser_factory(self.scm)
        tagged = tag_version(parser=parser,
                             package=self.package, file=self.file)
        print(f"tagged {tagged}")
