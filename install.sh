#!/bin/sh

# Install os dependencies:
if [ -f $(which apt-get) ]; then
    sudo apt-get install python-pip
else
    if [ -f $(which brew) ]; then
        brew install python
    fi
fi

# thefuck requires fresh versions of setuptools and pip:
sudo pip install -U pip setuptools
sudo pip install -U thefuck

# Setup aliases:
if [ -f ~/.bashrc ]; then
    echo 'eval $(thefuck --alias)' >> ~/.bashrc
fi

if [ -f ~/.bash_profile ]; then
    echo 'eval $(thefuck --alias)' >> ~/.bash_profile
fi

if [ -f ~/.zshrc ]; then
    echo 'eval $(thefuck --alias)' >> ~/.zshrc
fi

if [ -f ~/.config/fish/config.fish ]; then
    thefuck --alias >> ~/.config/fish/config.fish
fi

if [ -f ~/.tcshrc ]; then
    echo 'eval `thefuck --alias`' >> ~/.tcshrc
fi
