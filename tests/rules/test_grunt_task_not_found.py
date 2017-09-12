# -*- encoding: utf-8 -*-

from io import BytesIO
import pytest
from thefuck.types import Command
from thefuck.rules.grunt_task_not_found import match, get_new_command

output = '''
Warning: Task "{}" not found. Use --force to continue.

Aborted due to warnings.


Execution Time (2016-08-13 21:01:40 UTC+3)
loading tasks  11ms  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 92%
Total 12ms

'''.format

grunt_help_stdout = b'''
Grunt: The JavaScript Task Runner (v0.4.5)

Usage
 grunt [options] [task [task ...]]

Options
    --help, -h  Display this help text.
        --base  Specify an alternate base path. By default, all file paths are
                relative to the Gruntfile. (grunt.file.setBase) *
    --no-color  Disable colored output.
   --gruntfile  Specify an alternate Gruntfile. By default, grunt looks in the
                current or parent directories for the nearest Gruntfile.js or
                Gruntfile.coffee file.
   --debug, -d  Enable debugging mode for tasks that support it.
       --stack  Print a stack trace when exiting with a warning or fatal error.
   --force, -f  A way to force your way past warnings. Want a suggestion? Don't
                use this option, fix your code.
       --tasks  Additional directory paths to scan for task and "extra" files.
                (grunt.loadTasks) *
         --npm  Npm-installed grunt plugins to scan for task and "extra" files.
                (grunt.loadNpmTasks) *
    --no-write  Disable writing files (dry run).
 --verbose, -v  Verbose mode. A lot more information output.
 --version, -V  Print the grunt version. Combine with --verbose for more info.
  --completion  Output shell auto-completion rules. See the grunt-cli
                documentation for more information.

Options marked with * have methods exposed via the grunt API and should instead
be specified inside the Gruntfile wherever possible.

Available tasks
  autoprefixer  Prefix CSS files. *
    concurrent  Run grunt tasks concurrently *
         clean  Clean files and folders. *
       compass  Compile Sass to CSS using Compass *
        concat  Concatenate files. *
       connect  Start a connect web server. *
          copy  Copy files. *
        cssmin  Minify CSS *
       htmlmin  Minify HTML *
      imagemin  Minify PNG, JPEG, GIF and SVG images *
        jshint  Validate files with JSHint. *
        uglify  Minify files with UglifyJS. *
         watch  Run predefined tasks whenever watched files change.
       filerev  File revisioning based on content hashing *
        cdnify  Replace scripts with refs to the Google CDN *
         karma  run karma. *
         newer  Run a task with only those source files that have been modified
                since the last successful run.
     any-newer  DEPRECATED TASK.  Use the "newer" task instead
 newer-postrun  Internal task.
   newer-clean  Remove cached timestamps.
    ngAnnotate  Add, remove and rebuild AngularJS dependency injection
                annotations *
    ngconstant  Dynamic angular constant generator task. *
        svgmin  Minify SVG *
        usemin  Replaces references to non-minified scripts / stylesheets *
 useminPrepare  Using HTML markup as the primary source of information *
       wiredep  Inject Bower components into your source code. *
         serve  Compile then start a connect web server
        server  DEPRECATED TASK. Use the "serve" task instead
          test  Alias for "clean:server", "ngconstant:test", "wiredep",
                "concurrent:test", "autoprefixer", "connect:test", "karma"
                tasks.
         build  Alias for "ngconstant:production", "clean:dist", "wiredep",
                "useminPrepare", "concurrent:dist", "autoprefixer", "concat",
                "ngAnnotate", "copy:dist", "cdnify", "cssmin", "uglify",
                "filerev", "usemin", "htmlmin" tasks.
       default  Alias for "newer:jshint", "test", "build" tasks.

Tasks run in the order specified. Arguments may be passed to tasks that accept
them by using colons, like "lint:files". Tasks marked with * are "multi tasks"
and will iterate over all sub-targets if no argument is specified.

The list of available tasks may change based on tasks directories or grunt
plugins specified in the Gruntfile or via command-line options.

For more information, see http://gruntjs.com/
'''


@pytest.fixture(autouse=True)
def grunt_help(mocker):
    patch = mocker.patch('thefuck.rules.grunt_task_not_found.Popen')
    patch.return_value.stdout = BytesIO(grunt_help_stdout)
    return patch


@pytest.mark.parametrize('command', [
    Command('grunt defualt', output('defualt')),
    Command('grunt buld:css', output('buld:css'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('npm nuild', output('nuild')),
    Command('grunt rm', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (Command('grunt defualt', output('defualt')), 'grunt default'),
    (Command('grunt cmpass:all', output('cmpass:all')), 'grunt compass:all'),
    (Command('grunt cmpass:all --color', output('cmpass:all')),
     'grunt compass:all --color')])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
