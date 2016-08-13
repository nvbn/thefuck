from thefuck.utils import eager, get_closest, for_app


@for_app('fab')
def match(command):
    return 'Warning: Command(s) not found:' in command.stderr


# We need different behavior then in get_all_matched_commands.
@eager
def _get_between(content, start, end=None):
    should_yield = False
    for line in content.split('\n'):
        if start in line:
            should_yield = True
            continue

        if end and end in line:
            return

        if should_yield and line:
            yield line.strip().split(' ')[0]


def get_new_command(command):
    not_found_commands = _get_between(
        command.stderr, 'Warning: Command(s) not found:', 'Available commands:')
    possible_commands = _get_between(
        command.stdout, 'Available commands:')

    script = command.script
    for not_found in not_found_commands:
        fix = get_closest(not_found, possible_commands)
        script = script.replace(' {}'.format(not_found),
                                ' {}'.format(fix))

    return script
