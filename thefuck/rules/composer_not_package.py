import re
from thefuck.utils import for_app


@for_app("composer")
def match(command):
    # determine error type
    # matching "did you mean this" is not enough as composer also gives spelling suggestions for mistakes other than mispelled commands
    is_invalid_argument_exception = r"[InvalidArgumentException]" in command.output
    is_unable_to_find_package = (
        re.search(r"Could not find package (.*)\.", command.output) is not None
    )
    suggestions_present = "Did you mean" in command.output
    return (
        is_invalid_argument_exception
        and is_unable_to_find_package
        and suggestions_present
    )


def get_new_command(command):
    # because composer lets you install many packages at once, must look at output to determine the erroneous package name
    wrong_package_name = re.search(
        r"Could not find package (.*)\.", command.output
    ).group(1)
    offending_script_param = (
        wrong_package_name
        if (wrong_package_name in command.script_parts)
        else re.findall(r"{}:[^ ]+".format(wrong_package_name), command.script)[0]
    )
    version_constraint = offending_script_param[len(wrong_package_name) :]
    one_suggestion_only = "Did you mean this?" in command.output
    if one_suggestion_only:
        new_pkg = (
            re.search(r"Did you mean this\?[^\n]*\n\s*([^\n]*)", command.output)
            .group(1)
            .strip()
        )
        return command.script.replace(
            offending_script_param, new_pkg + version_constraint
        )
    # else there are multiple suggestions
    # trim output text to make it more digestable by regex
    trim_start_index = command.output.find("Did you mean")
    short_output = command.output[trim_start_index:]
    stripped_lines = [line.strip() for line in short_output.split("\n")]
    # each of the suggested packages can be found from index 1 to the first occurrence of a blank string
    end_index = stripped_lines.index("")
    suggested_packages = stripped_lines[1:end_index]
    return [
        command.script.replace(offending_script_param, pkg + version_constraint)
        for pkg in suggested_packages
    ]
