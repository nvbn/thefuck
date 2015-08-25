#!/bin/sh

should_add_alias () {
    [ -f $1 ] && ! grep -q thefuck $1
}

# Install os dependencies:
if [ -f $(which apt-get) ]; then
    sudo apt-get update
    sudo apt-get install python-pip
else
    if [ -f $(which brew) ]; then
        brew update
        brew install python
    fi
fi

# thefuck requires fresh versions of setuptools and pip:
sudo pip install -U pip setuptools
sudo pip install -U thefuck

# Setup aliases:
if should_add_alias ~/.bashrc; then
    echo 'eval $(thefuck --alias)' >> ~/.bashrc
fi

if should_add_alias ~/.bash_profile; then
    echo 'eval $(thefuck --alias)' >> ~/.bash_profile
fi

if should_add_alias ~/.zshrc; then
    echo 'eval $(thefuck --alias)' >> ~/.zshrc
fi

if should_add_alias ~/.config/fish/config.fish; then
    thefuck --alias >> ~/.config/fish/config.fish
fi

if should_add_alias ~/.tcshrc; then
    echo 'eval `thefuck --alias`' >> ~/.tcshrc
fi
