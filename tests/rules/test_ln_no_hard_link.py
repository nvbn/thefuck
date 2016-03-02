# -*- coding: utf-8 -*-

from thefuck.rules.ln_no_hard_link import match, get_new_command
from tests.utils import Command


def test_match():
    err = "hard link not allowed for directory"
    assert not match(Command())

    cmd1 = Command("ln barDir barLink", stderr="ln: ‘barDir’: {}".format(err))
    assert match(cmd1)

    cmd2 = Command("sudo ln a b", stderr="ln: ‘a’: {}".format(err))
    assert match(cmd2)

    cmd3 = Command("ln a b", stderr="... hard link")
    assert not match(cmd3)

    cmd4 = Command("sudo ln a b", stderr="... hard link")
    assert not match(cmd4)

    cmd5 = Command("a b", stderr=err)
    assert not match(cmd5)

    cmd6 = Command("sudo ln -nbi a b", stderr="ln: ‘a’: {}".format(err))
    assert match(cmd6)


def test_get_new_command():
    cmd1 = Command("ln barDir barLink")
    assert get_new_command(cmd1) == "ln -s barDir barLink"

    cmd2 = Command("sudo ln barDir barLink")
    assert get_new_command(cmd2) == "sudo ln -s barDir barLink"

    cmd3 = Command("sudo ln -nbi a b")
    assert get_new_command(cmd3) == "sudo ln -s -nbi a b"

    cmd4 = Command("ln -nbi a b && ls")
    assert get_new_command(cmd4) == "ln -s -nbi a b && ls"

    cmd5 = Command("ln a ln")
    assert get_new_command(cmd5) == "ln -s a ln"

    cmd6 = Command("sudo ln a ln")
    assert get_new_command(cmd6) == "sudo ln -s a ln"
