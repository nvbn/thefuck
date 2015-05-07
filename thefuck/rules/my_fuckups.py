
import thefuck.custom_fuckups

fuckups = custom_fuckups.get_fuckups()

def match(command, settings):
  if command in fuckups:
    return True
  return False # not found


def get_new_command(command, settings):
  return fuckups[command]

# priority = 1000  # Lower first
