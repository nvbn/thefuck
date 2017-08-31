import pytest
from thefuck.rules.mvn_unknown_lifecycle_phase import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('mvn cle', '[ERROR] Unknown lifecycle phase "cle". You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('mvn clean', """
[INFO] Scanning for projects...[INFO]                                                                         
[INFO] ------------------------------------------------------------------------
[INFO] Building test 0.2
[INFO] ------------------------------------------------------------------------
[INFO] 
[INFO] --- maven-clean-plugin:2.5:clean (default-clean) @ test ---
[INFO] Deleting /home/mlk/code/test/target
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 0.477s
[INFO] Finished at: Wed Aug 26 13:05:47 BST 2015
[INFO] Final Memory: 6M/240M
[INFO] ------------------------------------------------------------------------
"""),  # noqa
    Command('mvn --help', ''),
    Command('mvn -v', '')
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('mvn cle', '[ERROR] Unknown lifecycle phase "cle". You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]'), ['mvn clean', 'mvn compile']),
    (Command('mvn claen package', '[ERROR] Unknown lifecycle phase "claen". You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]'), ['mvn clean package'])])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
