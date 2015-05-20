import pytest
from thefuck.rules.django_south_ghost import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''Traceback (most recent call last):
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
  File "/home/nvbn/work/.../app/lib/south/migration/__init__.py", line 193, in migrate_app
    applied_all = check_migration_histories(applied_all, delete_ghosts, ignore_ghosts)
  File "/home/nvbn/work/.../app/lib/south/migration/__init__.py", line 88, in check_migration_histories
    raise exceptions.GhostMigrations(ghosts)
south.exceptions.GhostMigrations: 

 ! These migrations are in the database but not on disk:
    <tracker: 0033_auto__...>
    <tracker: 0034_fill_...>
    <tracker: 0035_rename_...>
    <qm_auth: 0003_add_...>
    <qm_auth: 0004_denormalize_...>
    <tracker: 0033_auto....>
    <tracker: 0034_fill...>
 ! I'm not trusting myself; either fix this yourself by fiddling
 ! with the south_migrationhistory table, or pass --delete-ghost-migrations
 ! to South to have it delete ALL of these records (this may not be good).
'''


def test_match(stderr):
    assert match(Command('./manage.py migrate', stderr=stderr), None)
    assert match(Command('python manage.py migrate', stderr=stderr), None)
    assert not match(Command('./manage.py migrate'), None)
    assert not match(Command('app migrate', stderr=stderr), None)
    assert not match(Command('./manage.py test', stderr=stderr), None)


def test_get_new_command():
    assert get_new_command(Command('./manage.py migrate auth'), None)\
        == './manage.py migrate auth --delete-ghost-migrations'
