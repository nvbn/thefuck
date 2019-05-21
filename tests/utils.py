from thefuck import types
from thefuck.const import DEFAULT_PRIORITY


class Rule(types.Rule):
    def __init__(self, name='', path='', match=lambda *_: True,
                 get_new_command=lambda *_: '',
                 post_match=lambda *_: '',
                 enabled_by_default=True,
                 side_effect=None,
                 priority=DEFAULT_PRIORITY,
                 requires_output=True,
                 is_post_match=False):
        super(Rule, self).__init__(name, path, match, get_new_command,
                                   post_match, enabled_by_default, side_effect,
                                   priority, requires_output, is_post_match)


class CorrectedCommand(types.CorrectedCommand):
    def __init__(self, script='', side_effect=None,
                 priority=DEFAULT_PRIORITY, rule=None):
        super(CorrectedCommand, self).__init__(
            script, side_effect, priority, rule)
