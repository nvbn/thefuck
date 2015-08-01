# -*- encoding: utf-8 -*-

from contextlib import contextmanager
from datetime import datetime
import sys
from traceback import format_exception
import colorama


def color(color_, settings):
    """Utility for ability to disabling colored output."""
    if settings.no_colors:
        return ''
    else:
        return color_


def exception(title, exc_info, settings):
    sys.stderr.write(
        u'{warn}[WARN] {title}:{reset}\n{trace}'
        u'{warn}----------------------------{reset}\n\n'.format(
            warn=color(colorama.Back.RED + colorama.Fore.WHITE
                       + colorama.Style.BRIGHT, settings),
            reset=color(colorama.Style.RESET_ALL, settings),
            title=title,
            trace=''.join(format_exception(*exc_info))))


def rule_failed(rule, exc_info, settings):
    exception('Rule {}'.format(rule.name), exc_info, settings)


def failed(msg, settings):
    sys.stderr.write('{red}{msg}{reset}\n'.format(
        msg=msg,
        red=color(colorama.Fore.RED, settings),
        reset=color(colorama.Style.RESET_ALL, settings)))


def show_corrected_command(corrected_command, settings):
    sys.stderr.write('{bold}{script}{reset}{side_effect}\n'.format(
        script=corrected_command.script,
        side_effect=' (+side effect)' if corrected_command.side_effect else '',
        bold=color(colorama.Style.BRIGHT, settings),
        reset=color(colorama.Style.RESET_ALL, settings)))


def confirm_text(corrected_command, multiple_cmds, settings):
    if multiple_cmds:
        arrows = '{blue}↑{reset}/{blue}↓{reset}/'
    else:
        arrows = ''

    sys.stderr.write(
        ('{clear}{bold}{script}{reset}{side_effect} '
         '[{green}enter{reset}/' + arrows + '{red}ctrl+c{reset}]').format(
            script=corrected_command.script,
            side_effect=' (+side effect)' if corrected_command.side_effect else '',
            clear='\033[1K\r',
            bold=color(colorama.Style.BRIGHT, settings),
            green=color(colorama.Fore.GREEN, settings),
            red=color(colorama.Fore.RED, settings),
            reset=color(colorama.Style.RESET_ALL, settings),
            blue=color(colorama.Fore.BLUE, settings)))


def debug(msg, settings):
    if settings.debug:
        sys.stderr.write(u'{blue}{bold}DEBUG:{reset} {msg}\n'.format(
            msg=msg,
            reset=color(colorama.Style.RESET_ALL, settings),
            blue=color(colorama.Fore.BLUE, settings),
            bold=color(colorama.Style.BRIGHT, settings)))


@contextmanager
def debug_time(msg, settings):
    started = datetime.now()
    try:
        yield
    finally:
        debug(u'{} took: {}'.format(msg, datetime.now() - started), settings)
