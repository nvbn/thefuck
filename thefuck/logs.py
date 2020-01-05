# -*- encoding: utf-8 -*-

from contextlib import contextmanager
from datetime import datetime
import sys
from traceback import format_exception
import colorama
from .conf import settings
from . import const


def color(color_):
    """Utility for ability to disabling colored output."""
    if settings.no_colors:
        return ''
    else:
        return color_


def warn(title):
    sys.stderr.write(u'{warn}[WARN] {title}{reset}\n'.format(
        warn=color(colorama.Back.RED + colorama.Fore.WHITE
                   + colorama.Style.BRIGHT),
        reset=color(colorama.Style.RESET_ALL),
        title=title))


def exception(title, exc_info):
    sys.stderr.write(
        u'{warn}[WARN] {title}:{reset}\n{trace}'
        u'{warn}----------------------------{reset}\n\n'.format(
            warn=color(colorama.Back.RED + colorama.Fore.WHITE
                       + colorama.Style.BRIGHT),
            reset=color(colorama.Style.RESET_ALL),
            title=title,
            trace=''.join(format_exception(*exc_info))))


def rule_failed(rule, exc_info):
    exception(u'Rule {}'.format(rule.name), exc_info)


def failed(msg):
    sys.stderr.write(u'{red}{msg}{reset}\n'.format(
        msg=msg,
        red=color(colorama.Fore.RED),
        reset=color(colorama.Style.RESET_ALL)))


def show_corrected_command(corrected_command):
    sys.stderr.write(u'{prefix}{bold}{script}{reset}{side_effect}\n'.format(
        prefix=const.USER_COMMAND_MARK,
        script=corrected_command.script,
        side_effect=u' (+side effect)' if corrected_command.side_effect else u'',
        bold=color(colorama.Style.BRIGHT),
        reset=color(colorama.Style.RESET_ALL)))


def confirm_text(corrected_command):
    sys.stderr.write(
        (u'{prefix}{clear}{bold}{script}{reset}{side_effect} '
         u'[{green}enter{reset}/{blue}↑{reset}/{blue}↓{reset}'
         u'/{red}ctrl+c{reset}]').format(
            prefix=const.USER_COMMAND_MARK,
            script=corrected_command.script,
            side_effect=' (+side effect)' if corrected_command.side_effect else '',
            clear='\033[1K\r',
            bold=color(colorama.Style.BRIGHT),
            green=color(colorama.Fore.GREEN),
            red=color(colorama.Fore.RED),
            reset=color(colorama.Style.RESET_ALL),
            blue=color(colorama.Fore.BLUE)))


def debug(msg):
    if settings.debug:
        sys.stderr.write(u'{blue}{bold}DEBUG:{reset} {msg}\n'.format(
            msg=msg,
            reset=color(colorama.Style.RESET_ALL),
            blue=color(colorama.Fore.BLUE),
            bold=color(colorama.Style.BRIGHT)))


@contextmanager
def debug_time(msg):
    started = datetime.now()
    try:
        yield
    finally:
        debug(u'{} took: {}'.format(msg, datetime.now() - started))


def how_to_configure_alias(configuration_details):
    print(u"Seems like {bold}fuck{reset} alias isn't configured!".format(
        bold=color(colorama.Style.BRIGHT),
        reset=color(colorama.Style.RESET_ALL)))

    if configuration_details:
        print(
            u"Please put {bold}{content}{reset} in your "
            u"{bold}{path}{reset} and apply "
            u"changes with {bold}{reload}{reset} or restart your shell.".format(
                bold=color(colorama.Style.BRIGHT),
                reset=color(colorama.Style.RESET_ALL),
                **configuration_details._asdict()))

        if configuration_details.can_configure_automatically:
            print(
                u"Or run {bold}fuck{reset} a second time to configure"
                u" it automatically.".format(
                    bold=color(colorama.Style.BRIGHT),
                    reset=color(colorama.Style.RESET_ALL)))

    print(u'More details - https://github.com/nvbn/thefuck#manual-installation')


def already_configured(configuration_details):
    print(
        u"Seems like {bold}fuck{reset} alias already configured!\n"
        u"For applying changes run {bold}{reload}{reset}"
        u" or restart your shell.".format(
            bold=color(colorama.Style.BRIGHT),
            reset=color(colorama.Style.RESET_ALL),
            reload=configuration_details.reload))


def configured_successfully(configuration_details):
    print(
        u"{bold}fuck{reset} alias configured successfully!\n"
        u"For applying changes run {bold}{reload}{reset}"
        u" or restart your shell.".format(
            bold=color(colorama.Style.BRIGHT),
            reset=color(colorama.Style.RESET_ALL),
            reload=configuration_details.reload))


def version(thefuck_version, python_version, shell_info):
    sys.stderr.write(
        u'The Fuck {} using Python {} and {}\n'.format(thefuck_version,
                                                       python_version,
                                                       shell_info))
