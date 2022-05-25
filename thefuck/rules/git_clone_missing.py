'''
Rule: git_clone_missing

Correct missing `git clone` command when pasting a git URL

```sh
& https://github.com/nvbn/thefuck.git
git clone https://github.com/nvbn/thefuck.git

Author: Miguel Guthridge
'''
from urllib import parse

output_contains = [
    'not found',
    'no such file or directory',
    'is not recognized as',
]


def match(command):
    # Ignore capitalisation in output
    output = command.output.lower()
    script = command.script
    # Check for a command not found error
    if not any([search in output for search in output_contains]):
        return False
    # URLs can't have spaces
    if ' ' in command.script:
        return False
    url = parse.urlparse(script, scheme='ssh')
    # HTTP URLs need a network address
    if not url.netloc and url.scheme != 'ssh':
        return False
    # SSH needs a username and a splitter between the path
    if url.scheme == 'ssh' and not ('@' in script and ':' in script):
        return False
    return url.scheme in ['http', 'https', 'ssh']


def get_new_command(command):
    return 'git clone ' + command.script
