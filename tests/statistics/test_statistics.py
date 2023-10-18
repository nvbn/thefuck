import pytest
import thefuck.const as const
from thefuck.types import CorrectedCommand
from thefuck.statistics import CommandRecords



class TestCommandRecords():
    def test_default(self):
        default = const.DEFAULT_RECORDS_DICT
        assert CommandRecords().statistics == default

    def test_clear_records(self):
        default = const.DEFAULT_RECORDS_DICT
        records = CommandRecords()
        records.statistics = {"not clear": "value"}
        records.clear_records() 
        assert records.statistics == default
        assert not records.statistics == {"not clear": "value"}

    def test_add_applied_rules(self):
        records = CommandRecords()
        commands = [
            CorrectedCommand('ls', None, 100),
            CorrectedCommand('git init', None, 200),
            CorrectedCommand('fuck', None, 300)]
        records.add_records(const.APPLIED_RULES, command_list = commands)
        assert records.statistics[const.APPLIED_RULES]['ls'] == 1
        assert records.statistics[const.APPLIED_RULES]['git init'] == 1
        assert records.statistics[const.APPLIED_RULES]['fuck'] == 1

        records.add_records(const.APPLIED_RULES, command_list = commands)
        assert records.statistics[const.APPLIED_RULES]['ls'] == 2
        assert records.statistics[const.APPLIED_RULES]['git init'] == 2
        assert records.statistics[const.APPLIED_RULES]['fuck'] == 2

        records.clear_records()

    def test_add_selected_rules(self):
        records = CommandRecords()
        command = CorrectedCommand('ls', None, 100)
        records.add_records(const.SELECTED_RULES, command_single = command)
        assert records.statistics[const.SELECTED_RULES]['ls'] == 1

        records.add_records(const.SELECTED_RULES, command_single = command)
        assert records.statistics[const.SELECTED_RULES]['ls'] == 2

        records.clear_records()

    def test_add_no_fucks_given(self):
        records = CommandRecords()
        records.clear_records()
        records.add_records(const.NO_FUCKS_GIVEN)
        assert records.statistics[const.NO_FUCKS_GIVEN] == 1

        records.add_records(const.NO_FUCKS_GIVEN)
        assert records.statistics[const.NO_FUCKS_GIVEN] == 2

        records.clear_records()



