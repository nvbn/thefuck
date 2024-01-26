import subprocess as sp

from thefuck.shells import shell
from thefuck.specific.git import git_support
from thefuck.utils import replace_argument


STDOUT_INDEX = 0


@git_support
def match(command):
    return (
        ("branch -d" in command.script or "branch -D" in command.script)
        and "error: Cannot delete branch '" in command.output
        and "' checked out at '" in command.output
    )


def get_sp_stdout(command):
    return sp.Popen(command, stdout=sp.PIPE, shell=True).communicate()[STDOUT_INDEX].strip().decode("utf-8")


@git_support
def get_new_command(command):
    remote_name = get_sp_stdout("git remote")
    default_branch_name = get_sp_stdout("git remote show {remote} | sed -n '/HEAD branch/s/.*: //p'".format(remote=remote_name))
    return shell.and_("git checkout {default_branch}".format(default_branch=default_branch_name), "{}").format(
        replace_argument(command.script, "-d", "-D")
    )
