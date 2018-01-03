from thefuck.utils import is_app, get_closest, replace_argument


# the most common ADB commands
_ADB_COMMANDS = [
    'devices',
    'install',
    'logcat',
    'pull',
    'push',
    'reboot',
    'shell',
    'uninstall'
]


def match(command):
    return (is_app(command, 'adb')
            and command.output.startswith('Android Debug Bridge version'))


def get_new_command(command):
    for idx, arg in enumerate(command.script_parts[1:]):
        # allowed params to ADB are d/e/s/p where s and p take additional args
        # for example 'adb -s 111 logcat' or 'adb -e logcat'
        if not arg[0] == '-' and not command.script_parts[idx] in ('-s', '-p'):
            adb_cmd = get_closest(arg, _ADB_COMMANDS)
            return replace_argument(command.script, arg, adb_cmd)
