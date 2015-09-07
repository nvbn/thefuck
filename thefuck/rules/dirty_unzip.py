import os
import zipfile
from thefuck.utils import for_app


def _is_bad_zip(file):
    with zipfile.ZipFile(file, 'r') as archive:
        return len(archive.namelist()) > 1


def _zip_file(command):
    # unzip works that way:
    # unzip [-flags] file[.zip] [file(s) ...] [-x file(s) ...]
    #                ^          ^ files to unzip from the archive
    #                archive to unzip
    for c in command.script.split()[1:]:
        if not c.startswith('-'):
            if c.endswith('.zip'):
                return c
            else:
                return '{}.zip'.format(c)


@for_app('unzip')
def match(command):
    return ('-d' not in command.script
            and _is_bad_zip(_zip_file(command)))


def get_new_command(command):
    return '{} -d {}'.format(command.script, _zip_file(command)[:-4])


def side_effect(old_cmd, command):
    with zipfile.ZipFile(_zip_file(old_cmd), 'r') as archive:
        for file in archive.namelist():
            try:
                os.remove(file)
            except OSError:
                # does not try to remove directories as we cannot know if they
                # already existed before
                pass


requires_output = False
