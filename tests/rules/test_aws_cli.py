import pytest

from thefuck.rules.aws_cli import match, get_new_command
from tests.utils import Command


no_suggestions = '''\
usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
To see help text, you can run:

  aws help
  aws <command> help
  aws <command> <subcommand> help
aws: error: argument command: Invalid choice, valid choices are:

dynamodb                                 | dynamodbstreams
ec2                                      | ecr
'''


misspelled_command = '''\
usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
To see help text, you can run:

  aws help
  aws <command> help
  aws <command> <subcommand> help
aws: error: argument command: Invalid choice, valid choices are:

dynamodb                                 | dynamodbstreams
ec2                                      | ecr


Invalid choice: 'dynamdb', maybe you meant:

  * dynamodb
'''


misspelled_subcommand = '''\
usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
To see help text, you can run:

  aws help
  aws <command> help
  aws <command> <subcommand> help
aws: error: argument operation: Invalid choice, valid choices are:

query                                    | scan
update-item                              | update-table


Invalid choice: 'scn', maybe you meant:

  * scan
'''


misspelled_subcommand_with_multiple_options = '''\
usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
To see help text, you can run:

  aws help
  aws <command> help
  aws <command> <subcommand> help
aws: error: argument operation: Invalid choice, valid choices are:

describe-table                           | get-item
list-tables                              | put-item


Invalid choice: 't-item', maybe you meant:

  * put-item
  * get-item
'''


@pytest.mark.parametrize('command', [
    Command('aws dynamdb scan', stderr=misspelled_command),
    Command('aws dynamodb scn', stderr=misspelled_subcommand),
    Command('aws dynamodb t-item',
            stderr=misspelled_subcommand_with_multiple_options)])
def test_match(command):
    assert match(command)


def test_not_match():
    assert not match(Command('aws dynamodb invalid', stderr=no_suggestions))


@pytest.mark.parametrize('command, result', [
    (Command('aws dynamdb scan', stderr=misspelled_command),
     ['aws dynamodb scan']),
    (Command('aws dynamodb scn', stderr=misspelled_subcommand),
     ['aws dynamodb scan']),
    (Command('aws dynamodb t-item',
             stderr=misspelled_subcommand_with_multiple_options),
     ['aws dynamodb put-item', 'aws dynamodb get-item'])])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
