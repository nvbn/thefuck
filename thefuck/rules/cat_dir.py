import gettext


def match(command):
    eisdir = gettext.translation('libc', fallback=True).gettext('Is a directory')
    return (
        command.script.startswith('cat') and
        command.output.startswith('cat: ') and
        command.output.rstrip().endswith(': %s' % eisdir)
    )


def get_new_command(command):
    return command.script.replace('cat', 'ls', 1)
