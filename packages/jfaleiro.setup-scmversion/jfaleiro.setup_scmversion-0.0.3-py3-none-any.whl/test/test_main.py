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
import contextlib
import os
from argparse import ArgumentParser

import pytest
from setup_scmversion.main import main
from setup_scmversion.parser import parser_factory, parsers


@pytest.fixture
def parser():
    return parser_factory()


def test_argparse_subparsers():
    parser = ArgumentParser()
    sp = parser.add_subparsers()
    sp_auto = sp.add_parser('auto')
    sp_auto.add_argument('--auto', action='store_true')
    sp_package = sp.add_parser('manual')
    sp_package.add_argument('package')
    sp_package.add_argument('file')
    parser.parse_args('auto --auto'.split())


def test_argparse_composite_choice():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--detect', action='store_true')
    group.add_argument('--manual', nargs=2)
    with pytest.raises(SystemExit):
        parser.parse_args('--manual'.split())
    parser.parse_args('--detect'.split())
    parser.parse_args('--manual package file'.split())


def test_argparse_composite_choice_simpler():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--auto', action='store_true')
    group.add_argument('package', nargs='?')
    parser.add_argument('file', nargs='?')
    parser.parse_args('--auto'.split())
    parser.parse_args('package file'.split())
    with pytest.raises(SystemExit) as e:
        parser.parse_args('--help'.split())
    assert e.value.code == 0


def test_main_help():
    with pytest.raises(SystemExit) as e:
        main(['--help'])
    assert e.value.code == 0
    with pytest.raises(SystemExit) as e1:
        main(['-h'])
    assert e1.value.code == 0


def test_main_invalid_command_arguments():
    with pytest.raises(SystemExit) as e1:
        main()
    assert e1.value.code == 2

    with pytest.raises(SystemExit) as e2:
        main(args=[''])
    assert e2.value.code == 2

    with pytest.raises(SystemExit) as e3:
        main(args=['--version'])
    assert e3.value.code == 2


def test_main_valid_version(parser, capsys):
    main(['version'])
    captured = capsys.readouterr()
    version = captured.out
    assert len(version) > 0
    assert version == parser.version() + "\n"


def test_main_version_type(parser, capsys):
    main(['version-type'])
    captured = capsys.readouterr()
    version_type = captured.out
    assert len(version_type) > 0
    assert version_type == parser.version_type().name + "\n"


def test_main_parsers(parser, capsys):
    main(['parsers'])
    captured = capsys.readouterr()
    p = captured.out
    assert len(p) > 0
    assert p == parsers() + "\n"


def test_main_tag_version(capsys):
    file_name = 'test/_version.py'
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_name)
    assert not os.path.exists(file_name)
    main(['tag-version', 'test'])
    assert os.path.exists(file_name)
    os.remove(file_name)
    captured = capsys.readouterr()
    p = captured.out
    assert p == "tagged ('test', '_version.py')\n"


def test_main_tag_version_default_package_default_file(capsys):
    file_name = 'setup_scmversion/_version.py'
    assert os.path.exists(file_name)
    original_creation_time = os.path.getmtime(file_name)
    main(['tag-version'])
    assert os.path.getmtime(file_name) >= original_creation_time
    captured = capsys.readouterr()
    p = captured.out
    assert p == "tagged ('setup_scmversion', '_version.py')\n"
