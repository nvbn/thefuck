#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: hostscli.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2017-02-05
"""

from thefuck.utils import for_app

no_command = "Error: No such command"
need_sudo = "hostscli.errors.SudoRequiredError"
no_website = "hostscli.errors.WebsiteImportError"


@for_app("hostscli")
def match(command):
    errors = [no_command, need_sudo, no_website]
    for error in errors:
        if error in command.stderr:
            return True
    return False


def get_new_command(command):
    if no_website in command.stderr:
        return ['hostscli websites']
    if need_sudo in command.stderr:
        return ['sudo {}'.format(command.script)]
    if no_command in command.stderr:
        return ['hostscli --help']
