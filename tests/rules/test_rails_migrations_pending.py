import pytest
from thefuck.rules.rails_migrations_pending import match, get_new_command
from thefuck.types import Command

output_env_development = '''
Migrations are pending. To resolve this issue, run:

        rails db:migrate RAILS_ENV=development
'''
output_env_test = '''
Migrations are pending. To resolve this issue, run:

        bin/rails db:migrate RAILS_ENV=test
'''


@pytest.mark.parametrize(
    "command",
    [
        Command("", output_env_development),
        Command("", output_env_test),
    ],
)
def test_match(command):
    assert match(command)


@pytest.mark.parametrize(
    "command",
    [
        Command("Environment data not found in the schema. To resolve this issue, run: \n\n", ""),
    ],
)
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize(
    "command, new_command",
    [
        (Command("bin/rspec", output_env_development), "rails db:migrate RAILS_ENV=development && bin/rspec"),
        (Command("bin/rspec", output_env_test), "bin/rails db:migrate RAILS_ENV=test && bin/rspec"),
    ],
)
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
