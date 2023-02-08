import re

from thefuck.utils import for_app


@for_app('heroku')
def match(command):
    return 'https://devcenter.heroku.com/articles/multiple-environments' in command.output


def get_new_command(command):
    apps = re.findall('([^ ]*) \\([^)]*\\)', command.output)
    return [command.script + ' --app ' + app for app in apps]
