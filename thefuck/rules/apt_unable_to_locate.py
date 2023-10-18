import subprocess

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, replace_command


@sudo_support
@for_app("apt", "apt-get")
def match(command):
    return "E: Unable to locate package" in command.output


def _parse_apt_search_results(search_text_lines):
    search_results = []

    for line in search_text_lines:
        line = line.decode().strip()
        if line.find("/") > 0:
            search_results.append(line.split("/")[0])

    return search_results


def _parse_apt_cache_search_results(search_text_lines):
    search_results = []

    for line in search_text_lines:
        line = line.decode().strip()
        if line.find(" - ") > 0:  # spaces are important
            search_results.append(line.split(" - ")[0])

    return search_results


def _get_search_results(app, command):
    _parser = _parse_apt_search_results

    if app == "apt-get":
        app = "apt-cache"
        _parser = _parse_apt_cache_search_results

    proc = subprocess.Popen(
        [app, "search", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    lines = proc.stdout.readlines()

    return _parser(lines)


@sudo_support
def get_new_command(command):
    invalid_operation = command.script_parts[-1]
    search_results = _get_search_results(command.script_parts[0], invalid_operation)

    return replace_command(command, invalid_operation, search_results)
