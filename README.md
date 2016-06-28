# The Fuck [![Version][version-badge]][version-link] [![Build Status][travis-badge]][travis-link] [![Windows Build Status][appveyor-badge]][appveyor-link] [![Coverage][coverage-badge]][coverage-link] [![MIT License][license-badge]](LICENSE.md)

Magnificent app which corrects your previous console command,
inspired by a [@liamosaur](https://twitter.com/liamosaur/)
[tweet](https://twitter.com/liamosaur/status/506975850596536320).

[![gif with examples][examples-link]][examples-link]

Few more examples:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
sudo apt-get install vim [enter/↑/↓/ctrl+c]
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
git push --set-upstream origin master [enter/↑/↓/ctrl+c]
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
python [enter/↑/↓/ctrl+c]
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...
```

```bash
➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
    branch

➜ fuck
git branch [enter/↑/↓/ctrl+c]
* master
```

```bash
➜ lein rpl
'rpl' is not a task. See 'lein help'.

Did you mean this?
         repl

➜ fuck
lein repl [enter/↑/↓/ctrl+c]
nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
REPL-y 0.3.1
...
```

If you are not scared to blindly run the changed command, there is a `require_confirmation`
[settings](#settings) option:

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

## Requirements

- python (2.7+ or 3.3+)
- pip
- python-dev

## Installation

On OS X you can install `The Fuck` with [Homebrew][homebrew]:

```bash
brew install thefuck
```

On Ubuntu you can install `The Fuck` with:
 
```bash
sudo apt update
sudo apt install python3-dev python3-pip
sudo -H pip3 install thefuck
```

On other systems you can install `The Fuck` with `pip`:

```bash
sudo -H pip install thefuck
```

[Or using an OS package manager (OS X, Ubuntu, Arch).](https://github.com/nvbn/thefuck/wiki/Installation)

You should place this command in your `.bash_profile`, `.bashrc`, `.zshrc` or other startup script:

```bash
eval "$(thefuck --alias)"
# You can use whatever you want as an alias, like for Mondays:
eval "$(thefuck --alias FUCK)"
```

[Or in your shell config (Bash, Zsh, Fish, Powershell, tcsh).](https://github.com/nvbn/thefuck/wiki/Shell-aliases)

Changes will be available only in a new shell session.
To make them available immediately, run `source ~/.bashrc` (or your shell config file like `.zshrc`).


## Update

```bash
sudo pip install thefuck --upgrade
```

**Aliases changed in 1.34.**

## How it works

The Fuck tries to match a rule for the previous command, creates a new command
using the matched rule and runs it. Rules enabled by default are as follows:

* `cargo` &ndash; runs `cargo build` instead of `cargo`;
* `cargo_no_command` &ndash; fixes wrongs commands like `cargo buid`;
* `cd_correction` &ndash; spellchecks and correct failed cd commands;
* `cd_mkdir` &ndash; creates directories before cd'ing into them;
* `cd_parent` &ndash; changes `cd..` to `cd ..`;
* `chmod_x` &ndash; add execution bit;
* `composer_not_command` &ndash; fixes composer command name;
* `cp_omitting_directory` &ndash; adds `-a` when you `cp` directory;
* `cpp11` &ndash; adds missing `-std=c++11` to `g++` or `clang++`;
* `dirty_untar` &ndash; fixes `tar x` command that untarred in the current directory;
* `dirty_unzip` &ndash; fixes `unzip` command that unzipped in the current directory;
* `django_south_ghost` &ndash; adds `--delete-ghost-migrations` to failed because ghosts django south migration;
* `django_south_merge` &ndash; adds `--merge` to inconsistent django south migration;
* `docker_not_command` &ndash; fixes wrong docker commands like `docker tags`;
* `dry` &ndash; fixes repetitions like `git git push`;
* `fix_alt_space` &ndash; replaces Alt+Space with Space character;
* `fix_file` &ndash; opens a file with an error in your `$EDITOR`;
* `git_add` &ndash; fixes *"pathspec 'foo' did not match any file(s) known to git."*;
* `git_branch_delete` &ndash; changes `git branch -d` to `git branch -D`;
* `git_branch_exists` &ndash; offers `git branch -d foo`, `git branch -D foo` or `git checkout foo` when creating a branch that already exists;
* `git_branch_list` &ndash; catches `git branch list` in place of `git branch` and removes created branch;
* `git_checkout` &ndash; fixes branch name or creates new branch;
* `git_diff_staged` &ndash; adds `--staged` to previous `git diff` with unexpected output;
* `git_fix_stash` &ndash; fixes `git stash` commands (misspelled subcommand and missing `save`);
* `git_help_aliased` &ndash; fixes `git help <alias>` commands replacing <alias> with the aliased command;
* `git_not_command` &ndash; fixes wrong git commands like `git brnch`;
* `git_pull` &ndash; sets upstream before executing previous `git pull`;
* `git_pull_clone` &ndash; clones instead of pulling when the repo does not exist;
* `git_push` &ndash; adds `--set-upstream origin $branch` to previous failed `git push`;
* `git_push_pull` &ndash; runs `git pull` when `push` was rejected;
* `git_rebase_no_changes` &ndash; runs `git rebase --skip` instead of `git rebase --continue` when there are no changes;
* `git_rm_recursive` &ndash; adds `-r` when you try to `rm` a directory;
* `git_remote_seturl_add` &ndash; runs `git remote add` when `git remote set_url` on nonexistant remote;
* `git_stash` &ndash; stashes you local modifications before rebasing or switching branch;
* `git_two_dashes` &ndash; adds a missing dash to commands like `git commit -amend` or `git rebase -continue`;
* `go_run` &ndash; appends `.go` extension when compiling/running Go programs;
* `grep_arguments_order` &ndash; fixes grep arguments order for situations like `grep -lir . test`;
* `grep_recursive` &ndash; adds `-r` when you trying to `grep` directory;
* `gulp_not_task` &ndash; fixes misspelled `gulp` tasks;
* `has_exists_script` &ndash; prepends `./` when script/binary exists;
* `heroku_not_command` &ndash; fixes wrong `heroku` commands like `heroku log`;
* `history` &ndash; tries to replace command with most similar command from history;
* `java` &ndash; removes `.java` extension when running Java programs;
* `javac` &ndash; appends missing `.java` when compiling Java files;
* `lein_not_task` &ndash; fixes wrong `lein` tasks like `lein rpl`;
* `ln_no_hard_link` &ndash; catches hard link creation on directories, suggest symbolic link;
* `ln_s_order` &ndash; fixes `ln -s` arguments order;
* `ls_lah` &ndash; adds `-lah` to `ls`;
* `man` &ndash; changes manual section;
* `man_no_space` &ndash; fixes man commands without spaces, for example `mandiff`;
* `mercurial` &ndash; fixes wrong `hg` commands;
* `mkdir_p` &ndash; adds `-p` when you trying to create directory without parent;
* `mvn_no_command` &ndash; adds `clean package` to `mvn`;
* `mvn_unknown_lifecycle_phase` &ndash; fixes misspelled lifecycle phases with `mvn`;
* `npm_wrong_command` &ndash; fixes wrong npm commands like `npm urgrade`;
* `no_command` &ndash; fixes wrong console commands, for example `vom/vim`;
* `no_such_file` &ndash; creates missing directories with `mv` and `cp` commands;
* `open` &ndash; prepends `http` to address passed to `open`;
* `pip_unknown_command` &ndash; fixes wrong `pip` commands, for example `pip instatl/pip install`;
* `python_command` &ndash; prepends `python` when you trying to run not executable/without `./` python script;
* `python_execute` &ndash; appends missing `.py` when executing Python files;
* `quotation_marks` &ndash; fixes uneven usage of `'` and `"` when containing args';
* `rm_dir` &ndash; adds `-rf` when you trying to remove directory;
* `sed_unterminated_s` &ndash; adds missing '/' to `sed`'s `s` commands;
* `sl_ls` &ndash; changes `sl` to `ls`;
* `ssh_known_hosts` &ndash; removes host from `known_hosts` on warning;
* `sudo` &ndash; prepends `sudo` to previous command if it failed because of permissions;
* `switch_lang` &ndash; switches command from your local layout to en;
* `systemctl` &ndash; correctly orders parameters of confusing `systemctl`;
* `test.py` &ndash; runs `py.test` instead of `test.py`;
* `touch` &ndash; creates missing directories before "touching";
* `tsuru_login` &ndash; runs `tsuru login` if not authenticated or session expired;
* `tsuru_not_command` &ndash; fixes wrong `tsuru` commands like `tsuru shell`;
* `tmux` &ndash; fixes `tmux` commands;
* `unknown_command` &ndash; fixes hadoop hdfs-style "unknown command", for example adds missing '-' to the command on `hdfs dfs ls`;
* `vagrant_up` &ndash; starts up the vagrant instance;
* `whois` &ndash; fixes `whois` command.

Enabled by default only on specific platforms:

* `apt_get` &ndash; installs app from apt if it not installed (requires `python-commandnotfound` / `python3-commandnotfound`);
* `apt_get_search` &ndash; changes trying to search using `apt-get` with searching using `apt-cache`;
* `apt_invalid_operation` &ndash; fixes invalid `apt` and `apt-get` calls, like `apt-get isntall vim`;
* `brew_install` &ndash; fixes formula name for `brew install`;
* `brew_unknown_command` &ndash; fixes wrong brew commands, for example `brew docto/brew doctor`;
* `brew_update_formula` &ndash; turns `brew update <formula>` into `brew upgrade <formula>`;
* `brew_upgrade` &ndash; appends `--all` to `brew upgrade` as per Homebrew's new behaviour;
* `pacman` &ndash; installs app with `pacman` if it is not installed (uses `yaourt` if available);
* `pacman_not_found` &ndash; fixes package name with `pacman` or `yaourt`.

Bundled, but not enabled by default:

* `git_push_force` &ndash; adds `--force-with-lease` to a `git push` (may conflict with `git_push_pull`);
* `rm_root` &ndash; adds `--no-preserve-root` to `rm -rf /` command.

## Creating your own rules

For adding your own rule you should create `your-rule-name.py`
in `~/.config/thefuck/rules`. The rule should contain two functions:

```python
match(command: Command) -> bool
get_new_command(command: Command) -> str | list[str]
```

Also the rule can contain an optional function

```python
side_effect(old_command: Command, fixed_command: str) -> None
```
and optional `enabled_by_default`, `requires_output` and `priority` variables.

`Command` has three attributes: `script`, `stdout` and `stderr`.

*Rules api changed in 3.0:* For accessing settings in rule you need to import it with `from thefuck.conf import settings`.
`settings` is a special object filled with `~/.config/thefuck/settings.py` and values from env ([see more below](#settings)).

Simple example of the rule for running script with `sudo`:

```python
def match(command):
    return ('permission denied' in command.stderr.lower()
            or 'EACCES' in command.stderr)


def get_new_command(command):
    return 'sudo {}'.format(command.script)

# Optional:
enabled_by_default = True

def side_effect(command, fixed_command):
    subprocess.call('chmod 777 .', shell=True)

priority = 1000  # Lower first, default is 1000

requires_output = True
```

[More examples of rules](https://github.com/nvbn/thefuck/tree/master/thefuck/rules),
[utility functions for rules](https://github.com/nvbn/thefuck/tree/master/thefuck/utils.py),
[app/os-specific helpers](https://github.com/nvbn/thefuck/tree/master/thefuck/specific/).

## Settings

The Fuck has a few settings parameters which can be changed in `$XDG_CONFIG_HOME/thefuck/settings.py` (`$XDG_CONFIG_HOME` defaults to `~/.config`):

* `rules` &ndash; list of enabled rules, by default `thefuck.conf.DEFAULT_RULES`;
* `exclude_rules` &ndash; list of disabled rules, by default `[]`;
* `require_confirmation` &ndash; requires confirmation before running new command, by default `True`;
* `wait_command` &ndash; max amount of time in seconds for getting previous command output;
* `no_colors` &ndash; disable colored output;
* `priority` &ndash; dict with rules priorities, rule with lower `priority` will be matched first;
* `debug` &ndash; enables debug output, by default `False`;
* `history_limit` &ndash; numeric value of how many history commands will be scanned, like `2000`;
* `alter_history` &ndash; push fixed command to history, by default `True`.

Example of `settings.py`:

```python
rules = ['sudo', 'no_command']
exclude_rules = ['git_push']
require_confirmation = True
wait_command = 10
no_colors = False
priority = {'sudo': 100, 'no_command': 9999}
debug = False
```

Or via environment variables:

* `THEFUCK_RULES` &ndash; list of enabled rules, like `DEFAULT_RULES:rm_root` or `sudo:no_command`;
* `THEFUCK_EXCLUDE_RULES` &ndash; list of disabled rules, like `git_pull:git_push`;
* `THEFUCK_REQUIRE_CONFIRMATION` &ndash; require confirmation before running new command, `true/false`;
* `THEFUCK_WAIT_COMMAND` &ndash; max amount of time in seconds for getting previous command output;
* `THEFUCK_NO_COLORS` &ndash; disable colored output, `true/false`;
* `THEFUCK_PRIORITY` &ndash; priority of the rules, like `no_command=9999:apt_get=100`,
rule with lower `priority` will be matched first;
* `THEFUCK_DEBUG` &ndash; enables debug output, `true/false`;
* `THEFUCK_HISTORY_LIMIT` &ndash; how many history commands will be scanned, like `2000`;
* `THEFUCK_ALTER_HISTORY` &ndash; push fixed command to history `true/false`.

For example:

```bash
export THEFUCK_RULES='sudo:no_command'
export THEFUCK_EXCLUDE_RULES='git_pull:git_push'
export THEFUCK_REQUIRE_CONFIRMATION='true'
export THEFUCK_WAIT_COMMAND=10
export THEFUCK_NO_COLORS='false'
export THEFUCK_PRIORITY='no_command=9999:apt_get=100'
export THEFUCK_HISTORY_LIMIT='2000'
```

## Developing

Install `The Fuck` for development:

```bash
pip install -r requirements.txt
python setup.py develop
```

Run unit tests:

```bash
py.test
```

Run unit and functional tests (requires docker):

```bash
py.test --enable-functional
```

For sending package to pypi:

```bash
sudo apt-get install pandoc
./release.py
```

## License MIT
Project License can be found [here](LICENSE.md).


[version-badge]:   https://img.shields.io/pypi/v/thefuck.svg?label=version
[version-link]:    https://pypi.python.org/pypi/thefuck/
[travis-badge]:    https://img.shields.io/travis/nvbn/thefuck.svg
[travis-link]:     https://travis-ci.org/nvbn/thefuck
[appveyor-badge]:  https://img.shields.io/appveyor/ci/nvbn/thefuck.svg?label=windows%20build
[appveyor-link]:   https://ci.appveyor.com/project/nvbn/thefuck
[coverage-badge]:  https://img.shields.io/coveralls/nvbn/thefuck.svg
[coverage-link]:   https://coveralls.io/github/nvbn/thefuck
[license-badge]:   https://img.shields.io/badge/license-MIT-007EC7.svg
[examples-link]:   https://raw.githubusercontent.com/nvbn/thefuck/master/example.gif
[homebrew]:        http://brew.sh/
