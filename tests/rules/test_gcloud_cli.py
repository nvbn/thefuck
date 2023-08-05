import pytest

from thefuck.rules.gcloud_cli import match, get_new_command
from thefuck.types import Command

no_suggestions = '''\
ERROR: (gcloud) Command name argument expected.
'''

misspelled_command = '''\
ERROR: (gcloud) Invalid choice: 'comute'.
Usage: gcloud [optional flags] <group | command>
  group may be           access-context-manager | ai-platform | alpha | app |
                         asset | auth | beta | bigtable | builds | components |
                         composer | compute | config | container | dataflow |
                         dataproc | datastore | debug | deployment-manager |
                         dns | domains | endpoints | filestore | firebase |
                         functions | iam | iot | kms | logging | ml |
                         ml-engine | organizations | projects | pubsub | redis |
                         resource-manager | scheduler | services | source |
                         spanner | sql | tasks | topic
  command may be         docker | feedback | help | info | init | version

For detailed information on this command and its flags, run:
  gcloud --help
'''

misspelled_subcommand = '''\
ERROR: (gcloud.compute) Invalid choice: 'instance'.
Maybe you meant:
  gcloud compute instance-groups
  gcloud compute instance-templates
  gcloud compute instances
  gcloud compute target-instances

To search the help text of gcloud commands, run:
  gcloud help -- SEARCH_TERMS
'''


@pytest.mark.parametrize('command', [
    Command('gcloud comute instances list', misspelled_subcommand),
    Command('gcloud compute instance list', misspelled_subcommand)])
def test_match(command):
    assert match(command)


def test_not_match():
    assert not match(Command('aws dynamodb invalid', no_suggestions))


@pytest.mark.parametrize('command, result', [
    (Command('gcloud comute instances list', misspelled_subcommand),
     ['gcloud compute instance-groups']),
    (Command('gcloud compute instance list', misspelled_subcommand),
     ['gcloud compute instance-groups'])])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
