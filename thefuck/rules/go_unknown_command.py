from thefuck.utils import get_closest, replace_argument

_GOLANG_COMMANDS = (
    "bug", "build", "clean", "doc", "env", "fix", "fmt", "generate", "get",
    "install", "list", "mod", "run", "test", "tool", "version", "vet")


def match(command):
    return (command.script_parts
            and command.script_parts[0] == "go"
            and 'unknown command' in command.output)


def get_new_command(command):
    closest_subcommand = get_closest(command.script_parts[1],
                                     _GOLANG_COMMANDS)
    return replace_argument(command.script, command.script_parts[1],
                            closest_subcommand)
