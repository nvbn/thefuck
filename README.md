# The Fuck [![Build Status](https://travis-ci.org/nvbn/thefuck.svg)](https://travis-ci.org/nvbn/thefuck)

**Aliases changed in 1.34.**

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

If you are scared to blindly run the changed command, there is a `require_confirmation`
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

- python (2.7+ or 3.3+)
- pip
- python-dev

## Installation

Install `The Fuck` with `pip`:

```bash
sudo pip install thefuck
```

[Or using an OS package manager (OS X, Ubuntu, Arch).](https://github.com/nvbn/thefuck/wiki/Installation)

And add to the `.bashrc` or `.bash_profile`(for OSX):

```bash
alias fuck='eval $(thefuck $(fc -ln -1)); history -r'
# You can use whatever you want as an alias, like for Mondays:
alias FUCK='fuck'
```

Or in your `.zshrc`:

```bash
alias fuck='eval $(thefuck $(fc -ln -1 | tail -n 1)); fc -R'
```

If you are using `tcsh`:
```tcsh
alias fuck 'set fucked_cmd=`history -h 2 | head -n 1` && eval `thefuck ${fucked_cmd}`'
```

Alternatively, you can redirect the output of `thefuck-alias`:

```bash
thefuck-alias >> ~/.bashrc
```

[Or in your shell config (Bash, Zsh, Fish, Powershell).](https://github.com/nvbn/thefuck/wiki/Shell-aliases)

Changes will be available only in a new shell session.
To make them available immediately, run `source ~/.bashrc` (or your shell config file like `.zshrc`).


## Update

```bash
sudo pip install thefuck --upgrade
```

## How it works

The Fuck tries to match a rule for the previous command, creates a new command
using the matched rule and runs it. Rules enabled by default are as follows:

* `cargo` &ndash; runs `cargo build` instead of `cargo`;
* `cargo_no_command` &ndash; fixes wrongs commands like `cargo buid`;
* `cd_correction` &ndash; spellchecks and correct failed cd commands;
* `cd_mkdir` &ndash; creates directories before cd'ing into them;
* `cd_parent` &ndash; changes `cd..` to `cd ..`;
* `composer_not_command` &ndash; fixes composer command name;
* `cp_omitting_directory` &ndash; adds `-a` when you `cp` directory;
* `cpp11` &ndash; add missing `-std=c++11` to `g++` or `clang++`;
* `django_south_ghost` &ndash; adds `--delete-ghost-migrations` to failed because ghosts django south migration;
* `django_south_merge` &ndash; adds `--merge` to inconsistent django south migration;
* `dry` &ndash; fix repetitions like "git git push";
* `fix_alt_space` &ndash; replaces Alt+Space with Space character;
* `git_add` &ndash; fix *"Did you forget to 'git add'?"*;
* `git_branch_list` &ndash; catches `git branch list` in place of `git branch` and removes created branch;
* `git_checkout` &ndash; creates the branch before checking-out;
* `git_diff_staged` &ndash; adds `--staged` to previous `git diff` with unexpected output;
* `git_no_command` &ndash; fixes wrong git commands like `git brnch`;
* `git_pull` &ndash; sets upstream before executing previous `git pull`;
* `git_push` &ndash; adds `--set-upstream origin $branch` to previous failed `git push`;
* `git_stash` &ndash; stashes you local modifications before rebasing or switching branch;
* `go_run` &ndash; appends `.go` extension when compiling/running Go programs
* `grep_recursive` &ndash; adds `-r` when you trying to grep directory;
* `has_exists_script` &ndash; prepends `./` when script/binary exists;
* `java` &ndash; removes `.java` extension when running Java programs;
* `javac` &ndash; appends missing `.java` when compiling Java files;
* `lein_not_task` &ndash; fixes wrong `lein` tasks like `lein rpl`;
* `ls_lah` &ndash; adds -lah to ls;
* `man` &ndash; change manual section;
* `man_no_space` &ndash; fixes man commands without spaces, for example `mandiff`;
* `mkdir_p` &ndash; adds `-p` when you trying to create directory without parent;
* `no_command` &ndash; fixes wrong console commands, for example `vom/vim`;
* `no_such_file` &ndash; creates missing directories with `mv` and `cp` commands;
* `open` &ndash; prepends `http` to address passed to `open`;
* `pip_unknown_command` &ndash; fixes wrong pip commands, for example `pip instatl/pip install`;
* `python_command` &ndash; prepends `python` when you trying to run not executable/without `./` python script;
* `python_execute` &ndash; appends missing `.py` when executing Python files;
* `quotation_marks` &ndash; fixes uneven usage of `'` and `"` when containing args'
* `rm_dir` &ndash; adds `-rf` when you trying to remove directory;
* `sl_ls` &ndash; changes `sl` to `ls`;
* `ssh_known_hosts` &ndash; removes host from `known_hosts` on warning;
* `sudo` &ndash; prepends `sudo` to previous command if it failed because of permissions;
* `switch_layout` &ndash; switches command from your local layout to en;
* `systemctl` &ndash; correctly orders parameters of confusing systemctl;
* `test.py` &ndasg; runs `py.test` instead of `test.py`;
* `whois` &ndash; fixes `whois` command.

Enabled by default only on specific platforms:

* `apt_get` &ndash; installs app from apt if it not installed;
* `brew_install` &ndash; fixes formula name for `brew install`;
* `brew_unknown_command` &ndash; fixes wrong brew commands, for example `brew docto/brew doctor`;
* `brew_upgrade` &ndash; appends `--all` to `brew upgrade` as per Homebrew's new behaviour
* `pacman` &ndash; installs app with `pacman` or `yaourt` if it is not installed.

Bundled, but not enabled by default:

* `rm_root` &ndash; adds `--no-preserve-root` to `rm -rf /` command.

## Creating your own rules

For adding your own rule you should create `your-rule-name.py`
in `~/.thefuck/rules`. Rule should contain two functions:
`match(command: Command, settings: Settings) -> bool`
and `get_new_command(command: Command, settings: Settings) -> str`.
Also the rule can contain optional function
`side_effect(command: Command, settings: Settings) -> None` and
optional boolean `enabled_by_default`.

`Command` has three attributes: `script`, `stdout` and `stderr`.

`Settings` is a special object filled with `~/.thefuck/settings.py` and values from env, [more](#settings).

Simple example of the rule for running script with `sudo`:

```python
def match(command, settings):
    return ('permission denied' in command.stderr.lower()
            or 'EACCES' in command.stderr)


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)

# Optional:
enabled_by_default = True

def side_effect(command, settings):
    subprocess.call('chmod 777 .', shell=True)

priority = 1000  # Lower first
```

[More examples of rules](https://github.com/nvbn/thefuck/tree/master/thefuck/rules),
[utility functions for rules](https://github.com/nvbn/thefuck/tree/master/thefuck/utils.py).

## Settings

The Fuck has a few settings parameters which can be changed in `~/.thefuck/settings.py`:

* `rules` &ndash; list of enabled rules, by default `thefuck.conf.DEFAULT_RULES`;
* `require_confirmation` &ndash; requires confirmation before running new command, by default `False`;
* `wait_command` &ndash; max amount of time in seconds for getting previous command output;
* `no_colors` &ndash; disable colored output;
* `priority` &ndash; dict with rules priorities, rule with lower `priority` will be matched first.

Example of `settings.py`:

```python
rules = ['sudo', 'no_command']
require_confirmation = True
wait_command = 10
no_colors = False
priority = {'sudo': 100, 'no_command': 9999}
```

Or via environment variables:

* `THEFUCK_RULES` &ndash; list of enabled rules, like `DEFAULT_RULES:rm_root` or `sudo:no_command`;
* `THEFUCK_REQUIRE_CONFIRMATION` &ndash; require confirmation before running new command, `true/false`;
* `THEFUCK_WAIT_COMMAND` &ndash; max amount of time in seconds for getting previous command output;
* `THEFUCK_NO_COLORS` &ndash; disable colored output, `true/false`;
* `THEFUCK_PRIORITY` &ndash; priority of the rules, like `no_command=9999:apt_get=100`,
rule with lower `priority` will be matched first.

For example:

```bash
export THEFUCK_RULES='sudo:no_command'
export THEFUCK_REQUIRE_CONFIRMATION='true'
export THEFUCK_WAIT_COMMAND=10
export THEFUCK_NO_COLORS='false'
export THEFUCK_PRIORITY='no_command=9999:apt_get=100'
```

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
