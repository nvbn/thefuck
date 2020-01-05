import pytest
from thefuck.rules.terraform_init import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, output', [
    ('terraform plan', 'Error: Initialization required. '
                       'Please see the error message above.'),
    ('terraform plan', 'This module is not yet installed. Run "terraform init" '
                       'to install all modules required by this configuration.'),
    ('terraform apply', 'Error: Initialization required. '
                        'Please see the error message above.'),
    ('terraform apply', 'This module is not yet installed. Run "terraform init" '
                        'to install all modules required by this configuration.')])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('terraform --version', 'Terraform v0.12.2'),
    ('terraform plan', 'No changes. Infrastructure is up-to-date.'),
    ('terraform apply', 'Apply complete! Resources: 0 added, 0 changed, 0 destroyed.'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))


@pytest.mark.parametrize('command, new_command', [
    (Command('terraform plan', ''), 'terraform init && terraform plan'),
    (Command('terraform apply', ''), 'terraform init && terraform apply'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
