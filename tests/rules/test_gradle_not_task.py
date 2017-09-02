import pytest
from io import BytesIO
from thefuck.rules.gradle_no_task import match, get_new_command
from thefuck.types import Command

gradle_tasks = b'''
:tasks

------------------------------------------------------------
All tasks runnable from root project
------------------------------------------------------------

Android tasks
-------------
androidDependencies - Displays the Android dependencies of the project.
signingReport - Displays the signing info for each variant.
sourceSets - Prints out all the source sets defined in this project.

Build tasks
-----------
assemble - Assembles all variants of all applications and secondary packages.
assembleAndroidTest - Assembles all the Test applications.
assembleDebug - Assembles all Debug builds.
assembleRelease - Assembles all Release builds.
build - Assembles and tests this project.
buildDependents - Assembles and tests this project and all projects that depend on it.
buildNeeded - Assembles and tests this project and all projects it depends on.
compileDebugAndroidTestSources
compileDebugSources
compileDebugUnitTestSources
compileReleaseSources
compileReleaseUnitTestSources
extractDebugAnnotations - Extracts Android annotations for the debug variant into the archive file
extractReleaseAnnotations - Extracts Android annotations for the release variant into the archive file
mockableAndroidJar - Creates a version of android.jar that's suitable for unit tests.

Build Setup tasks
-----------------
init - Initializes a new Gradle build. [incubating]
wrapper - Generates Gradle wrapper files. [incubating]

Help tasks
----------
components - Displays the components produced by root project 'org.rerenderer_example.snake'. [incubating]
dependencies - Displays all dependencies declared in root project 'org.rerenderer_example.snake'.
dependencyInsight - Displays the insight into a specific dependency in root project 'org.rerenderer_example.snake'.
help - Displays a help message.
model - Displays the configuration model of root project 'org.rerenderer_example.snake'. [incubating]
projects - Displays the sub-projects of root project 'org.rerenderer_example.snake'.
properties - Displays the properties of root project 'org.rerenderer_example.snake'.
tasks - Displays the tasks runnable from root project 'org.rerenderer_example.snake' (some of the displayed tasks may belong to subprojects).

Install tasks
-------------
installDebug - Installs the Debug build.
installDebugAndroidTest - Installs the android (on device) tests for the Debug build.
installRelease - Installs the Release build.
uninstallAll - Uninstall all applications.
uninstallDebug - Uninstalls the Debug build.
uninstallDebugAndroidTest - Uninstalls the android (on device) tests for the Debug build.
uninstallRelease - Uninstalls the Release build.

React tasks
-----------
bundleDebugJsAndAssets - bundle JS and assets for Debug.
bundleReleaseJsAndAssets - bundle JS and assets for Release.

Verification tasks
------------------
check - Runs all checks.
clean - Deletes the build directory.
connectedAndroidTest - Installs and runs instrumentation tests for all flavors on connected devices.
connectedCheck - Runs all device checks on currently connected devices.
connectedDebugAndroidTest - Installs and runs the tests for debug on connected devices.
deviceAndroidTest - Installs and runs instrumentation tests using all Device Providers.
deviceCheck - Runs all device checks using Device Providers and Test Servers.
lint - Runs lint on all variants.
lintDebug - Runs lint on the Debug build.
lintRelease - Runs lint on the Release build.
test - Run unit tests for all variants.
testDebugUnitTest - Run unit tests for the debug build.
testReleaseUnitTest - Run unit tests for the release build.

Other tasks
-----------
assembleDefault
copyDownloadableDepsToLibs
jarDebugClasses
jarReleaseClasses

To see all tasks and more detail, run gradlew tasks --all

To see more detail about a task, run gradlew help --task <task>

BUILD SUCCESSFUL

Total time: 1.936 secs
'''

output_not_found = '''

FAILURE: Build failed with an exception.

* What went wrong:
Task '{}' not found in root project 'org.rerenderer_example.snake'.

* Try:
Run gradlew tasks to get a list of available tasks. Run with --stacktrace option to get the stack trace. Run with --info or --debug option to get more log output.
'''.format

output_ambiguous = '''

FAILURE: Build failed with an exception.

* What went wrong:
Task '{}' is ambiguous in root project 'org.rerenderer_example.snake'. Candidates are: 'assembleRelease', 'assembleReleaseUnitTest'.

* Try:
Run gradlew tasks to get a list of available tasks. Run with --stacktrace option to get the stack trace. Run with --info or --debug option to get more log output.
'''.format


@pytest.fixture(autouse=True)
def tasks(mocker):
    patch = mocker.patch('thefuck.rules.gradle_no_task.Popen')
    patch.return_value.stdout = BytesIO(gradle_tasks)
    return patch


@pytest.mark.parametrize('command', [
    Command('./gradlew assembler', output_ambiguous('assembler')),
    Command('./gradlew instar', output_not_found('instar')),
    Command('gradle assembler', output_ambiguous('assembler')),
    Command('gradle instar', output_not_found('instar'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('./gradlew assemble', ''),
    Command('gradle assemble', ''),
    Command('npm assembler', output_ambiguous('assembler')),
    Command('npm instar', output_not_found('instar'))])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (Command('./gradlew assembler', output_ambiguous('assembler')),
     './gradlew assemble'),
    (Command('./gradlew instardebug', output_not_found('instardebug')),
     './gradlew installDebug'),
    (Command('gradle assembler', output_ambiguous('assembler')),
     'gradle assemble'),
    (Command('gradle instardebug', output_not_found('instardebug')),
     'gradle installDebug')])
def test_get_new_command(command, result):
    assert get_new_command(command)[0] == result
