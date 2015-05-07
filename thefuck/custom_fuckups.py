
# handle reading and writing local list of fuckups

# fuckups are stored in ~/.thefuck/my_fuckups

# file format:
#   fucked up command
#   fixed command
#   fucked up command
#   fixed command
#   ...

# rule is in rules/myfuckups.py

# TODO default fuckups (could replace some existing rules with these, mostly typo rules) in ~/.thefuck/my_fuckups

def get_fuckups(): # returns a dictionary of your fuckups from ~/.thefuck/my_fuckups
  
  FILENAME = '~/.thefuck/my_fuckups'
  FILE = open(FILENAME, 'r')

  IS_FUCKUP = True

  fuckups = dict()
  
  for line in FILE:
    if IS_FUCKUP:
      key = line
      IS_FUCKUP = False
    else:
      cmd = line
      IS_FUCKUP = True
      fuckups[key] = cmd
  
  FILE.close()

  return fuckups

def add_fuckup(fucked, fixed):

  print ('Adding fucked: ' + fucked + ' as fixed: ' + fixed)

  FILENAME = '~/.thefuck/my_fuckups'
  FILE = open(FILENAME, 'w')

  FILE.write(fucked + '\n')
  FILE.write(fixed + '\n')

  FILE.close()

  return

def remove_fuckup(fuckup):

  print ('Removing fucked: ' + fucked + ' as fixed: ' + fixed)

  FILENAME = '~/.thefuck/my_fuckups'
  FILE = open(FILENAME, 'r')

  fuckup_cmd = ''

  lines = FILE.readlines()

  FILE.close 
 
  FILE = open(FILENAME, 'w')

  for number, line in enumerate(lines):
    if line != fuckup and line != fuckup_cmd:
      FILE.write(line)
    elif line == fuckup:
      fuckup_cmd = lines[number + 1]

  FILE.close()

  return
