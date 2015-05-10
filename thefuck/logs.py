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


def show_command(new_command, side_effect, settings):
    sys.stderr.write('{bold}{command}{side_effect}{reset}\n'.format(
        command=new_command,
        side_effect='*' if side_effect else '',
        bold=color(colorama.Style.BRIGHT, settings),
        reset=color(colorama.Style.RESET_ALL, settings)))


def confirm_command(new_command, side_effect, settings):
    sys.stderr.write(
        '{bold}{command}{side_effect}{reset} '
        '[{green}enter{reset}/{red}ctrl+c{reset}]'.format(
            command=new_command,
            side_effect='*' if side_effect else '',
            bold=color(colorama.Style.BRIGHT, settings),
            green=color(colorama.Fore.GREEN, settings),
            red=color(colorama.Fore.RED, settings),
            reset=color(colorama.Style.RESET_ALL, settings)))
    sys.stderr.flush()


def failed(msg, settings):
    sys.stderr.write('{red}{msg}{reset}\n'.format(
        msg=msg,
        red=color(colorama.Fore.RED, settings),
        reset=color(colorama.Style.RESET_ALL, settings)))
