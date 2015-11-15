import pytest
from thefuck.rules.mvn_no_command import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='mvn', stdout='[ERROR] No goals have been specified for this build. You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='mvn clean', stdout="""
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
"""),
    Command(script='mvn --help'),
    Command(script='mvn -v')
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(script='mvn', stdout='[ERROR] No goals have been specified for this build. You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]'), ['mvn clean package', 'mvn clean install']),
    (Command(script='mvn -N', stdout='[ERROR] No goals have been specified for this build. You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]'), ['mvn -N clean package', 'mvn -N clean install'])])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
