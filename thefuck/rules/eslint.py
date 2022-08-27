import re, os
from thefuck.utils import replace_argument, for_app


def match(command):
    return 'ESLint couldn\'t find the plugin' in command.output

ex = os.path.exists

eslint_regex = re.compile("ESLint couldn't find the plugin \"([^\"]+)\"")

def get_node_package_manager_install_dev():
    if ex("yarn.lock"):
        return "yarn add --dev"
    return "npm i -D"


def get_new_command(command):
    package = eslint_regex.search(command.output).group(1)

    if not package:
        return None

    npm = get_node_package_manager_install_dev()

    if not npm:
        return None
    
    return npm + " " + package
