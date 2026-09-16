from thefuck.utils import which

enabled_by_default = bool(which('xcodebuild'))


def _is_license_command(command):
    return command.script_parts[:2] == ['xcodebuild', '-license']


def match(command):
    return ("sudo xcodebuild -license" in command.output
            and command.script_parts[:1] != ['sudo'])


def get_new_command(command):
    if _is_license_command(command):
        return [u'sudo {}'.format(command.script)]

    return [u'sudo xcodebuild -license accept && {}'.format(command.script),
            u'sudo xcodebuild -license && {}'.format(command.script)]
