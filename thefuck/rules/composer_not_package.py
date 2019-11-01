import re
from thefuck.utils import replace_argument, for_app


@for_app('composer')
def match(command):
    # determine error type
    # matching "did you mean this" is not enough as composer also gives spelling suggestions for mistakes other than mispelled commands
    is_invalid_argument_exception = r"[InvalidArgumentException]" in command.output
    is_unable_to_find_package = re.search(r"Could not find package (.*)\.", command.output) is not None
    suggestions_present = (('did you mean this?' in command.output.lower()
                            or 'did you mean one of these?' in command.output.lower()))
    return is_invalid_argument_exception and is_unable_to_find_package and suggestions_present


def get_new_command(command):
    # because composer lets you install many packages at once, must look at output to determine the erroneous package name
    wrong_package_name = re.search(r"Could not find package (.*)\.", command.output).group(1)
    offending_script_param = wrong_package_name if (wrong_package_name in command.script_parts) else re.findall(
        r"{}:[^ ]+".format(wrong_package_name), command.script)[0]
    version_constraint = offending_script_param[len(wrong_package_name):]
    one_suggestion_only = 'did you mean this?' in command.output.lower()
    if one_suggestion_only:
        # wrong regex??
        new_cmd = re.findall(r'Did you mean this\?[^\n]*\n\s*([^\n]*)', command.output)
        return replace_argument(command.script, offending_script_param, new_cmd[0].strip() + version_constraint)
    else:
        # there are multiple suggestions
        # trim output text to make it more digestable by regex
        trim_start_index = command.output.find("Did you mean one of these?")
        short_output = command.output[trim_start_index:]
        stripped_lines = [line.strip() for line in short_output.split("\n")]
        # each of the suggested commands can be found from index 1 to the first occurence of blank string
        try:
            end_index = stripped_lines.index('')
        except ValueError:
            end_index = None
        suggested_commands = stripped_lines[1:end_index]
        return [
            replace_argument(command.script, offending_script_param, cmd + version_constraint)
            for cmd in suggested_commands
        ]
