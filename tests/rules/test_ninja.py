import pytest
from thefuck.rules.ninja import get_new_command, match
from thefuck.types import Command

match_output = 'ninja: error: unknown target \'clong\', did you mean \'clang\'?'
no_match_output = 'ninja: error: unknown target \'foobar\''

def test_match():
  assert match(Command('ninja clong', match_output))
  assert not match(Command('ninja foobar', no_match_output))

def test_get_new_command():
  new_command = get_new_command(Command('ninja clong', match_output))
  assert new_command == 'ninja clang'
