import pytest
from thefuck.rules.django_south_merge import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return '''Running migrations for app:
 ! Migration app:0003_auto... should not have been applied before app:0002_auto__add_field_query_due_date_ but was.
Traceback (most recent call last):
  File "/home/nvbn/work/.../bin/python", line 42, in <module>
    exec(compile(__file__f.read(), __file__, "exec"))
  File "/home/nvbn/work/.../app/manage.py", line 34, in <module>
    execute_from_command_line(sys.argv)
  File "/home/nvbn/work/.../lib/django/core/management/__init__.py", line 443, in execute_from_command_line
    utility.execute()
  File "/home/nvbn/work/.../lib/django/core/management/__init__.py", line 382, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/nvbn/work/.../lib/django/core/management/base.py", line 196, in run_from_argv
    self.execute(*args, **options.__dict__)
  File "/home/nvbn/work/.../lib/django/core/management/base.py", line 232, in execute
    output = self.handle(*args, **options)
  File "/home/nvbn/work/.../app/lib/south/management/commands/migrate.py", line 108, in handle
    ignore_ghosts = ignore_ghosts,
  File "/home/nvbn/work/.../app/lib/south/migration/__init__.py", line 207, in migrate_app
    raise exceptions.InconsistentMigrationHistory(problems)
south.exceptions.InconsistentMigrationHistory: Inconsistent migration history
The following options are available:
    --merge: will just attempt the migration ignoring any potential dependency conflicts.
'''


def test_match(output):
    assert match(Command('./manage.py migrate', output))
    assert match(Command('python manage.py migrate', output))
    assert not match(Command('./manage.py migrate', ''))
    assert not match(Command('app migrate', output))
    assert not match(Command('./manage.py test', output))


def test_get_new_command():
    assert (get_new_command(Command('./manage.py migrate auth', ''))
            == './manage.py migrate auth --merge')
