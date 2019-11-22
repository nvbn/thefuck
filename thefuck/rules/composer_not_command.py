import re
from thefuck.utils import for_app


@for_app("composer")
def match(command):
    # determine error type
    # matching "did you mean this" is not enough as composer also gives spelling suggestions for mistakes other than mispelled commands
    is_undefined_command_error = "CommandNotFoundException" in command.output
    suggestions_present = "Did you mean" in command.output
    return is_undefined_command_error and suggestions_present


def get_new_command(command):
    # since the command class already tells us the original argument, we need not resort to regex
    broken_cmd = command.script_parts[1]
    one_suggestion_only = "Did you mean this?" in command.output
    if one_suggestion_only:
        new_cmd = (
            re.search(r"Did you mean this\?[^\n]*\n\s*([^\n]*)", command.output)
            .group(1)
            .strip()
        )
        return command.script.replace(broken_cmd, new_cmd)
    # else there are multiple suggestions
    # trim output text to make it more digestable by regex
    trim_start_index = command.output.find("Did you mean")
    short_output = command.output[trim_start_index:]
    stripped_lines = [line.strip() for line in short_output.split("\n")]
    # each of the suggested commands can be found from index 1 to the first occurrence of a blank string
    end_index = stripped_lines.index("")
    suggested_commands = stripped_lines[1:end_index]
    return [
        command.script.replace(broken_cmd, cmd.strip()) for cmd in suggested_commands
    ]
