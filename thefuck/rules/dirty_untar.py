from thefuck import shells
import os
import tarfile


def _is_tar_extract(cmd):
    if '--extract' in cmd:
        return True

    cmd = cmd.split()

    return len(cmd) > 1 and 'x' in cmd[1]


def _tar_file(cmd):
    tar_extensions = ('.tar', '.tar.Z', '.tar.bz2', '.tar.gz', '.tar.lz',
                      '.tar.lzma', '.tar.xz', '.taz', '.tb2', '.tbz', '.tbz2',
                      '.tgz', '.tlz', '.txz', '.tz')

    for c in cmd.split():
        for ext in tar_extensions:
            if c.endswith(ext):
                return (c, c[0:len(c)-len(ext)])


def match(command, settings):
    return (command.script.startswith('tar')
            and '-C' not in command.script
            and _is_tar_extract(command.script)
            and _tar_file(command.script) is not None)


def get_new_command(command, settings):
    return shells.and_('mkdir -p {dir}', '{cmd} -C {dir}') \
                 .format(dir=_tar_file(command.script)[1], cmd=command.script)


def side_effect(old_cmd, command, settings):
    with tarfile.TarFile(_tar_file(old_cmd.script)[0]) as archive:
        for file in archive.getnames():
            os.remove(file)
