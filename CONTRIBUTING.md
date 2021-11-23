# Report issues
If you have any issue with The Fuck, sorry about that, but we will do what we
can to fix that. Actually, maybe we already have, so first thing to do is to
update The Fuck and see if the bug is still there.

If it is (sorry again), check if the problem has not already been reported and
if not, just open an issue on [GitHub](https://github.com/nvbn/thefuck) with
the following basic information:
  - the output of `thefuck --version` (something like `The Fuck 3.1 using
    Python 3.5.0`);
  - your shell and its version (`bash`, `zsh`, *Windows PowerShell*, etc.);
  - your system (Debian 7, ArchLinux, Windows, etc.);
  - how to reproduce the bug;
  - the output of The Fuck with `THEFUCK_DEBUG=true` exported (typically execute
    `export THEFUCK_DEBUG=true` in your shell before The Fuck);
  - if the bug only appears with a specific application, the output of that
    application and its version;
  - anything else you think is relevant.

It's only with enough information that we can do something to fix the problem.

# Make a pull request
We gladly accept pull request on the [official
repository](https://github.com/nvbn/thefuck) for new rules, new features, bug
fixes, etc.

# Developing

In order to develop locally, there are two options:

- Develop using a local installation of Python 3 and setting up a virtual environment
- Develop using an automated VSCode Dev Container.

## Develop using local Python installation

[Create and activate a Python 3 virtual environment.](https://docs.python.org/3/tutorial/venv.html)

Install `The Fuck` for development:

```bash
pip install -r requirements.txt
python setup.py develop
```

Run code style checks:

```bash
flake8
```

Run unit tests:

```bash
pytest
```

Run unit and functional tests (requires docker):

```bash
pytest --enable-functional
```

For sending package to pypi:

```bash
sudo apt-get install pandoc
./release.py
```

## Develop using Dev Container

To make local development easier a [VSCode Devcontainer](https://code.visualstudio.com/docs/remote/remote-overview) is included with this repository. This will allows you to spin up a Docker container with all the necessary prerequisites for this project pre-installed ready to go, no local Python install/setup required.

### Prerequisites

To use the container you require:
- [Docker](https://www.docker.com/products/docker-desktop)
- [VSCode](https://code.visualstudio.com/)
- [VSCode Remote Development Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
- [Windows Users Only]: [Installation of WSL2 and configuration of Docker to use it](https://docs.docker.com/docker-for-windows/wsl/)

Full notes about [installation are here](https://code.visualstudio.com/docs/remote/containers#_installation)

### Running the container

Assuming you have the prerequisites:

1. Open VSCode
1. Open command palette (CMD+SHIFT+P (mac) or CTRL+SHIFT+P (windows))
1. Select `Remote-Containers: Reopen in Container`.
1. Container will be built, install all pip requirements and your VSCode will mount into it automagically.
1. Your VSCode and container now essentially become a throw away environment.
