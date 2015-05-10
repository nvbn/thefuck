import pytest
from thefuck.rules.composer_not_command import match, get_new_command
from tests.utils import Command


@pytest.fixture
def composer_not_command():
    return """

                                    
  [InvalidArgumentException]        
  Command "udpate" is not defined.  
  Did you mean this?                
      update


"""


@pytest.fixture
def composer_not_command_one_of_this():
    return """
                            


  [InvalidArgumentException]       
  Command "pdate" is not defined.  
  Did you mean one of these?       
      selfupdate                   
      self-update                  
      update                       



"""


def test_match(composer_not_command, composer_not_command_one_of_this):
    assert match(Command('composer udpate',
                         stderr=composer_not_command), None)
    assert match(Command('composer pdate',
                         stderr=composer_not_command_one_of_this), None)
    assert not match(Command('ls update', stderr=composer_not_command),
                     None)


def test_get_new_command(composer_not_command, composer_not_command_one_of_this):
    assert get_new_command(Command('composer udpate',
                                   stderr=composer_not_command), None) \
           == 'composer update'
    assert get_new_command(
        Command('composer pdate', stderr=composer_not_command_one_of_this),
        None) == 'composer selfupdate'
