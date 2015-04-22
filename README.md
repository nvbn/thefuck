# The Fuck [![Build Status](https://travis-ci.org/nvbn/thefuck.svg)](https://travis-ci.org/nvbn/thefuck)

Magnificent app which corrects your previous console command,
inspired by a [@liamosaur](https://twitter.com/liamosaur/)
[tweet](https://twitter.com/liamosaur/status/506975850596536320).

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
```

```bash
➜ git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master


➜ fuck
git push --set-upstream origin master
Counting objects: 9, done.
...
```

```bash
➜ puthon
No command 'puthon' found, did you mean:
 Command 'python' from package 'python-minimal' (main)
 Command 'python' from package 'python3' (main)
zsh: command not found: puthon

➜ fuck
python
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...
```

```bash
➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
	branch

➜ fuck
git branch
* master
```

```bash
➜ lein rpl
'rpl' is not a task. See 'lein help'.

Did you mean this?
         repl

➜ fuck
lein repl
nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
REPL-y 0.3.1
...
```

If you are scared to blindly run changed command, there's `require_confirmation`
[settings](#settings) option:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
sudo apt-get install vim [Enter/Ctrl+C]
[sudo] password for nvbn:
Reading package lists... Done
...
```

## Requirements

- pip
- python
- python-dev

## Installation

Install `The Fuck` with `pip`:

```bash
sudo pip install thefuck
```

If it fails try to use `easy_install`:

```bash
sudo easy_install thefuck
```

And add to `.bashrc` or `.zshrc` or `.bash_profile`(for OSX):

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

Or in your Powershell `$PROFILE` on Windows:

```powershell
function fuck { 
    $fuck = $(thefuck (get-history -count 1).commandline)
    if($fuck.startswith("echo")) { 
        $fuck.substring(5) 
    } 
    else { iex "$fuck" } 
}
```

Changes will be available only in a new shell session.


## Update

```bash
sudo pip install thefuck --upgrade
```

## How it works

The Fuck tries to match rule for the previous command, create new command
using matched rule and run it. Rules enabled by default:

* `cd_parent` &ndash; changes `cd..` to `cd ..`;
* `cp_omitting_directory` &ndash; adds `-a` when you `cp` directory;
* `git_no_command` &ndash; fixes wrong git commands like `git brnch`;
* `git_push` &ndash; adds `--set-upstream origin $branch` to previous failed `git push`;
* `has_exists_script` &ndash; prepends `./` when script/binary exists;
* `lein_not_task` &ndash; fixes wrong `lein` tasks like `lein rpl`;
* `mkdir_p` &ndash; adds `-p` when you trying to create directory without parent;
* `no_command` &ndash; fixes wrong console commands, for example `vom/vim`;
* `python_command` &ndash; prepends `python` when you trying to run not executable/without `./` python script;
* `rm_dir` &ndash; adds `-rf` when you trying to remove directory;
* `sudo` &ndash; prepends `sudo` to previous command if it failed because of permissions;
* `switch_layout` &ndash; switches command from your local layout to en.

## Creating your own rules

For adding your own rule you should create `your-rule-name.py`
in `~/.thefuck/rules`. Rule should contain two functions:
`match(command: Command, settings: Settings) -> bool`
and `get_new_command(command: Command, settings: Settings) -> str`.

`Command` has three attributes: `script`, `stdout` and `stderr`.

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

The Fuck has a few settings parameters, they can be changed in `~/.thefuck/settings.py`:

* `rules` &ndash; list of enabled rules, by default all;
* `require_confirmation` &ndash; require confirmation before running new command, by default `False`; 
* `wait_command` &ndash; max amount of time in seconds for getting previous command output;
* `no_colors` &ndash; disable colored output.

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
Project License can be found [here](LICENSE.md).
