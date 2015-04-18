# The Fuck [![Build Status](https://travis-ci.org/nvbn/thefuck.svg)](https://travis-ci.org/nvbn/thefuck)

Magnificent app which corrects your previous console command,
inspired by [@liamosaur](https://twitter.com/liamosaur/status/506975850596536320)
twit.

Few examples:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
sudo apt-get install vim
[sudo] password for nvbn:
Reading package lists... Done
...

➜ git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master


➜ fuck
git push --set-upstream origin master
Counting objects: 9, done.
...

➜ puthon
No command 'puthon' found, did you mean:
 Command 'python' from package 'python-minimal' (main)
 Command 'python' from package 'python3' (main)
zsh: command not found: puthon

➜ fuck
python
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...

➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
	branch

➜ fuck
git branch
* master

➜ lein rpl
'rpl' is not a task. See 'lein help'.

Did you mean this?
         repl

➜ fuck
nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
REPL-y 0.3.1
...
```

## Installation

Install `The Fuck` with `pip`:

```bash
sudo pip install thefuck
```

If it fails try to use `easy_install`:

```bash
sudo easy_intall thefuck
```

And add to `.bashrc` or `.zshrc`:

```bash
alias fuck='$(thefuck $(fc -ln -1))'
# You can use whatever you want as an alias, like for mondays:
alias FUCK='fuck'
```

Or in `config.fish`:

```fish
function fuck
    eval (thefuck $history[1])
end
```

Changes will available only in a new shell session.

## How it works

The Fuck tries to match rule for the previous command, create new command
using matched rule and run it. Rules enabled by default:

* `git_no_command` &ndash; fixes wrong git commands like `git brnch`;
* `git_push` &ndash; adds `--set-upstream origin $branch` to previous failed `git push`;
* `no_command` &ndash; fixes wrong console commands, for example `vom/vim`;
* `sudo` &ndash; prepends `sudo` to previous command if it failed because of permissions.  

## Creating your own rules

For adding your own rule you should create `your-rule-name.py`
in `~/.thefuck/rules`. Rule should contain two functions:
`match(command: Command, settings: Settings) -> bool`
and `get_new_command(command: Command, settings: Settings) -> str`.

`Command` have three attributes: `script`, `stdout` and `stderr`.

`Settings` is `~/.thefuck/settings.py`.

Simple example of the rule for running script with `sudo`:

```python
def match(command, settings):
    return ('permission denied' in command.stderr.lower()
            or 'EACCES' in command.stderr)


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)
```

[More examples of rules](https://github.com/nvbn/thefuck/tree/master/thefuck/rules),
[utility functions for rules](https://github.com/nvbn/thefuck/tree/master/thefuck/utils.py).

## Settings

The Fuck have a few settings parameters:

* `rules` &ndash; list of enabled rules, by default all;
* `wait_command` &ndash; max amount of time in seconds for getting previous command output;
* `command_not_found` &ndash; path to `command_not_found` binary,
by default `/usr/lib/command-not-found`.

## Developing

Install `The Fuck` for development:

```bash
pip install -r requirements.txt
python setup.py develop
```

Run tests:

```bash
py.test
```

## License MIT
