import pytest
from thefuck.rules.terraform_no_command import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, output', [
    ('terraform appyl', 'Terraform has no command named "appyl". Did you mean "apply"?'),
    ('terraform destory', 'Terraform has no command named "destory". Did you mean "destroy"?')])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('terraform --version', 'Terraform v0.12.2'),
    ('terraform plan', 'No changes. Infrastructure is up-to-date.'),
    ('terraform apply', 'Apply complete! Resources: 0 added, 0 changed, 0 destroyed.'),
])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, new_command', [
    ('terraform appyl', 'Terraform has no command named "appyl". Did you mean "apply"?', 'terraform apply',),
    ('terraform destory --some-other-option', 'Terraform has no command named "destory". Did you mean "destroy"?', 'terraform destroy --some-other-option',),
])
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
