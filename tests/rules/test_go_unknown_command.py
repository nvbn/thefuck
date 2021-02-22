import pytest
from io import BytesIO
from thefuck.rules.go_unknown_command import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def build_misspelled_output():
    return '''go bulid: unknown command
Run 'go help' for usage.'''


@pytest.fixture
def go_stderr(mocker):
    stderr = b'''Go is a tool for managing Go source code.

Usage:

\tgo <command> [arguments]

The commands are:

\tbug         start a bug report
\tbuild       compile packages and dependencies
\tclean       remove object files and cached files
\tdoc         show documentation for package or symbol
\tenv         print Go environment information
\tfix         update packages to use new APIs
\tfmt         gofmt (reformat) package sources
\tgenerate    generate Go files by processing source
\tget         add dependencies to current module and install them
\tinstall     compile and install packages and dependencies
\tlist        list packages or modules
\tmod         module maintenance
\trun         compile and run Go program
\ttest        test packages
\ttool        run specified go tool
\tversion     print Go version
\tvet         report likely mistakes in packages

Use "go help <command>" for more information about a command.

Additional help topics:

\tbuildconstraint build constraints
\tbuildmode       build modes
\tc               calling between Go and C
\tcache           build and test caching
\tenvironment     environment variables
\tfiletype        file types
\tgo.mod          the go.mod file
\tgopath          GOPATH environment variable
\tgopath-get      legacy GOPATH go get
\tgoproxy         module proxy protocol
\timportpath      import path syntax
\tmodules         modules, module versions, and more
\tmodule-get      module-aware go get
\tmodule-auth     module authentication using go.sum
\tmodule-private  module configuration for non-public modules
\tpackages        package lists and patterns
\ttestflag        testing flags
\ttestfunc        testing functions

Use "go help <topic>" for more information about that topic.

'''
    mock = mocker.patch('subprocess.Popen')
    mock.return_value.stderr = BytesIO(stderr)
    return mock


def test_match(build_misspelled_output):
    assert match(Command('go bulid', build_misspelled_output))


def test_not_match():
    assert not match(Command('go run', 'go run: no go files listed'))


@pytest.mark.usefixtures('no_memoize', 'go_stderr')
def test_get_new_command(build_misspelled_output):
    assert get_new_command(Command('go bulid', build_misspelled_output)) == 'go build'
