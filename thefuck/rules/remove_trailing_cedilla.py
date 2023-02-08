# -*- encoding: utf-8 -*-

CEDILLA = "ç"


def match(command):
    return command.script.endswith(CEDILLA)


def get_new_command(command):
    return command.script[:-1]
