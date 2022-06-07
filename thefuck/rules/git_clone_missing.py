'''
Rule: git_clone_missing

Correct missing `git clone` command when pasting a git URL

```sh
>>> https://github.com/nvbn/thefuck.git
git clone https://github.com/nvbn/thefuck.git
```

Author: Miguel Guthridge
'''
from six.moves.urllib import parse


def match(command):
    script = command.script
    parts = command.script_parts
    # We want it to be a URL by itself
    if len(parts) > 1:
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
