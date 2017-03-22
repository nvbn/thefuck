import re

fix = 'git commit -m "Initial commit." && {command}'
refspec_does_not_match = re.compile(r'src refspec \w+ does not match any\.')


def match(command):
    if refspec_does_not_match.search(command.stderr):
        return True

    return False


def get_new_command(command):
    return fix.format(command=command.script)
