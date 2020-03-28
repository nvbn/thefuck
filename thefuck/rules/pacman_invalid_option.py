from thefuck.specific.archlinux import archlinux_env
import re


def match(command):
    return "error: invalid option '-s'" in command.output


def get_new_command(command):
    opt = re.findall(r" -[dqrstuf]", command.script)[0]
    return re.sub(opt, opt.upper(), command.script)


enabled_by_default = archlinux_env()
