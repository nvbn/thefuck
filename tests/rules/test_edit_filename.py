import os

import pytest

from thefuck.rules.edit_filename import EDITORS, get_new_command, match
from thefuck.types import Command

parametrize_editor = pytest.mark.parametrize("editor", EDITORS)


def _edit_command(editor, path):
    return Command(editor + " " + str(path), "")


@parametrize_editor
def test_correct_file_no_match(tmp_path, editor):
    f = tmp_path / "module.py"
    f.touch()
    assert not match(_edit_command(editor, f))


@parametrize_editor
def test_similar_correct_file(tmp_path, editor):
    f = tmp_path / "module.py"
    f2 = tmp_path / "module.html"
    f.touch()
    f2.touch()
    assert not match(_edit_command(editor, f))


@parametrize_editor
def test_match_for_nonexisting(tmp_path, editor):
    f = tmp_path / "module.py"
    edited = tmp_path / "module"
    f.touch()
    assert match(_edit_command(editor, edited))


@parametrize_editor
def test_match_for_nonexisting_editor_flag(tmp_path, editor):
    f = tmp_path / "module.py"
    edited = tmp_path / "module"
    f.touch()
    assert match(_edit_command(editor + " --servername server", edited))


def test_match_for_nonexisting_bad_editor(tmp_path):
    f = tmp_path / "module.py"
    edited = tmp_path / "module"
    f.touch()
    assert not match(_edit_command("cat", edited))


@parametrize_editor
def test_get_new_command(tmp_path, editor):
    f = tmp_path / "module.py"
    edited = tmp_path / "module"
    f.touch()
    assert get_new_command(_edit_command(editor, edited)) == [
        _edit_command(editor, f).script
    ]


@parametrize_editor
def test_get_new_command_multiple(tmp_path, editor):
    f = tmp_path / "module.py"
    f2 = tmp_path / "module.html"
    edited = tmp_path / "module"
    f.touch()
    f2.touch()
    assert sorted(get_new_command(_edit_command(editor, edited))) == sorted(
        [_edit_command(editor, f).script, _edit_command(editor, f2).script]
    )


@parametrize_editor
def test_get_new_command_for_nonexisting_editor_flag(tmp_path, editor):
    f = tmp_path / "module.py"
    edited = tmp_path / "module"
    f.touch()
    assert get_new_command(_edit_command(editor + " --servername server", edited)) == [
        _edit_command(editor + " --servername server", f).script
    ]
