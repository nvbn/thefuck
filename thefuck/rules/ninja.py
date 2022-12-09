import re

def match(command):
  return 'unknown target' in command.output and 'did you mean' in command.output

def get_new_command(command):
  target = re.search(r'did you mean \'(.*)\'\?$', command.output).group(1)
  return 'ninja {}'.format(target)
