import pytest
from thefuck.rules.xcode_license import match, get_new_command
from thefuck.types import Command


admin_output = (
    "Agreeing to the Xcode and Apple SDKs license requires admin privileges, "
    "please accept the Xcode license as the root user "
    "(e.g. 'sudo xcodebuild -license').\n")

not_agreed_output = (
    "You have not agreed to the Xcode license agreements, please run "
    "'sudo xcodebuild -license' from within a Terminal window to review "
    "and agree to the Xcode license agreements.\n")


@pytest.mark.parametrize('script, output', [
    ('git clone https://github.com/nvbn/thefuck.git', admin_output),
    ('git status', not_agreed_output),
    ('make', not_agreed_output),
    ('xcodebuild -license', admin_output)])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('git clone https://github.com/nvbn/thefuck.git', ''),
    ('git status', 'fatal: not a git repository'),
    ('sudo xcodebuild -license', admin_output),
    ('sudo xcodebuild -license accept', admin_output)])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, new_command', [
    ('git clone https://github.com/nvbn/thefuck.git', admin_output,
     ['sudo xcodebuild -license accept && git clone https://github.com/nvbn/thefuck.git',
      'sudo xcodebuild -license && git clone https://github.com/nvbn/thefuck.git']),
    ('git status', not_agreed_output,
     ['sudo xcodebuild -license accept && git status',
      'sudo xcodebuild -license && git status']),
    ('xcodebuild -license', admin_output,
     ['sudo xcodebuild -license']),
    ('xcodebuild -license accept', admin_output,
     ['sudo xcodebuild -license accept'])])
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
