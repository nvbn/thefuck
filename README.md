# The Fuck

Magnificent app which corrects your previous console command,
inspired by [@liamosaur](https://twitter.com/liamosaur/status/506975850596536320)
twit.

Few examples:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
[sudo] password for nvbn: 
Reading package lists... Done
...

➜ git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master


➜ fuck
Counting objects: 9, done.
...

➜ puthon
No command 'puthon' found, did you mean:
 Command 'python' from package 'python-minimal' (main)
 Command 'python' from package 'python3' (main)
zsh: command not found: puthon

➜ fuck
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...
```

## Installation

Install `The Fuck`:

```bash
sudo pip3 install thefuck
```

And add to `.bashrc` or `.zshrc`:

```bash
alias fuck='$(thefuck $(fc -ln -1))'
```

## Developing

Install `The Fuck` for development:

```bash
pip3 install -r requirements.txt
python3 setup.py develop
```

Run tests:

```bash
py.test
```
