from thefuck.shells import shell
from thefuck.utils import for_app


@for_app("cp", "mv")
def match(command):
    return (
        "No such file or directory" in command.output
        or command.output.startswith("cp: directory")
        and command.output.rstrip().endswith("does not exist")
    )


def get_new_command(command):
    return shell.and_(u"mkdir -p {}".format(command.script_parts[-1]), command.script)
