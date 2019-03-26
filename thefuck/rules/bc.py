"""
Check for misspelled "bc" (basic calculator) command and correct it.
"""
def match(command):
   return (
      command.script.startswith(('bv', 'cb', 'vc', 'bb')) and
      len(command.script.split(' ')[0]) == 2 and
      'not found' in command.output
   )


def get_new_command(command):
   _command =  command.script.split(' ')
   _command[0] = 'bc'
   return ' '.join(_command)
