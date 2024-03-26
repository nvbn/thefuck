import pytest
import os
from thefuck.rules.makefile import match, get_new_command
from thefuck.types import Command

@pytest.mark.parametrize('command,expected', [
    (Command('make fo', "make: *** No rule to make target 'fo'.  Stop."), True),
    (Command('make ba', "make: *** No rule to make target 'ba'.  Stop."), True),
    (Command('mak foo', "mak: command not found"), True),
    (Command('mak oo', "mak: command not found"), True),
    (Command('meak foo', "meak: command not found"), True),
    (Command('maek bar', "maek: command not found"), True),
    (Command('maek br', "maek: command not found"), True),
    (Command('amke foo', "amke: command not found"), True),
    (Command('make foo', "make: command not found"), False),
    (Command('cd foo', 'cd: foo: No such file or directory'), False),
    (Command('java foo.java', 'error message'), False),
    (Command('make partone parttwo', "make: *** No rule to make target 'partone parttwo'.  Stop."), True)
    ])
def test_match(command,expected):
    """
    Tests the match function with inputs such as misspelled makes,
    misspelled targets, irrelevant commands, and correctly formatted commands.
    Tests with makefiles named Makefile, makefile, and GNUmakefile
    """
    with open("Makefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("bar:\n")
    result = match(command)
    os.remove("Makefile") # Removes Temporary Makefile
    assert result == expected

    with open("makefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("bar:\n")
    result = match(command)
    os.remove("makefile") # Removes Temporary Makefile
    assert result == expected

    with open("GNUmakefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("bar:\n")
    result = match(command)
    os.remove("GNUmakefile") # Removes Temporary Makefile
    assert result == expected



@pytest.mark.parametrize('command,expected', [
    (Command('make foo', "no error"), False),
    (Command('make fo', "make: *** No rule to make target 'fo'.  Stop."), False),
    (Command('maek bar', "maek: command not found"), False),
    (Command('cd foo', 'cd: foo: No such file or directory'), False)
    ])
def test_match_no_makefile(command,expected):
    """
    Tests the match function with no available makefile
    """
    result = match(command)
    assert result == expected


@pytest.mark.parametrize('command,expected', [
    (Command('make fo', "make: *** No rule to make target 'fo'.  Stop."), "make foo"),
    (Command('make ba', "make: *** No rule to make target 'ba'.  Stop."), "make bar"),
    (Command('make for', "make: *** No rule to make target 'for'.  Stop."), "make foo"),
    (Command('mak foo', "mak: command not found"), "make foo"),
    (Command('mak oo', "mak: command not found"), "make foo"),
    (Command('meak foo', "meak: command not found"), "make foo"),
    (Command('maek bar', "maek: command not found"), "make bar"),
    (Command('maek br', "maek: command not found"), "make bar"),
    (Command('amke foo', "amke: command not found"), "make foo"),
    (Command('amke qwe', "amke: command not found"), "make foo"),
    ])
def test_get_new_command(command,expected):
    """ 
    Test the correct functionality of generating the new command. 
    Tests with makefiles named Makefile, makefile, and GNUmakefile
    """

    with open("Makefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("\tg++ testfoo.cpp\n")
        openfile.write("bar:\n")
        openfile.write("\tg++ testbar.cpp\n")
    result = get_new_command(command)
    os.remove("Makefile") # Removes Temporary Makefile
    assert result == expected

    with open("makefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("\tg++ testfoo.cpp\n")
        openfile.write("bar:\n")
        openfile.write("\tg++ testbar.cpp\n")
    result = get_new_command(command)
    os.remove("makefile") # Removes Temporary Makefile
    assert result == expected

    with open("GNUmakefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("\tg++ testfoo.cpp\n")
        openfile.write("bar:\n")
        openfile.write("\tg++ testbar.cpp\n")
    result = get_new_command(command)
    os.remove("GNUmakefile") # Removes Temporary Makefile
    assert result == expected

@pytest.mark.parametrize('command,expected', [
    (Command('make fo', "make: *** No rule to make target 'fo'.  Stop."), "make foo"),
    (Command('make foodo', "make: *** No rule to make target 'foodo'.  Stop."), "make food"),
    (Command('make dfoo', "make: *** No rule to make target 'dfoo'.  Stop."), "make foo"),
    ])
def test_get_new_command_2(command,expected):
    with open("Makefile", "w") as openfile:
        # Creates Temporary makefile for testing
        openfile.write("foo:\n")
        openfile.write("\tg++ testfoo.cpp\n")
        openfile.write("food:\n")
        openfile.write("\tg++ testfood.cpp\n")
    result = get_new_command(command)
    os.remove("Makefile") # Removes Temporary Makefile
    assert result == expected
    