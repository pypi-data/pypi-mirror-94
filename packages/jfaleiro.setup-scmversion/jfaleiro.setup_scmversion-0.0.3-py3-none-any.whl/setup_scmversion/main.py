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
import argparse
import sys

from .parser import Tags, parser_factory, parsers, tag_version


def main(args=sys.argv[1:]):
    version_parser = parser_factory()
    commands = {
        'version': lambda _: version_parser.version(),
        'version-type': lambda _: version_parser.version_type().name,
        'parsers': lambda _: parsers(),
        'tag-version': lambda args:
        f"tagged {tag_version(package=args.package, file=args.file)}",
    }

    parser = argparse.ArgumentParser(description='Version parser from scm')
    sub_parsers = parser.add_subparsers(required=True, dest='command')

    sub_parsers.add_parser(
        'version',
        help='displays the version')
    sub_parsers.add_parser(
        'version-type',
        help=f'displays the version type (one of {[e.name for e in Tags]})')
    sub_parsers.add_parser(
        'parsers',
        help='lists all parsers available')
    tag_parser = sub_parsers.add_parser(
        'tag-version',
        help='tag the package with the version')
    group = tag_parser.add_mutually_exclusive_group()
    group.add_argument(
        '--auto',
        help='autodetect package name',
        action='store_true')
    group.add_argument(
        'package', nargs='?',
        help='name of the package')
    tag_parser.add_argument(
        'file',
        help='name of the file',
        nargs='?',
        default='_version')
    args = parser.parse_args(args)
    print(commands[args.command](args))


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
