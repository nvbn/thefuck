from thefuck.types import SortedCorrectedCommandsSequence
from tests.utils import CorrectedCommand


class TestSortedCorrectedCommandsSequence(object):
    def test_realises_generator_only_on_demand(self, settings):
        should_realise = False

        def gen():
            yield CorrectedCommand('git commit')
            yield CorrectedCommand('git branch', priority=200)
            assert should_realise
            yield CorrectedCommand('git checkout', priority=100)

        commands = SortedCorrectedCommandsSequence(gen())
        assert commands[0] == CorrectedCommand('git commit')
        should_realise = True
        assert commands[1] == CorrectedCommand('git checkout', priority=100)
        assert commands[2] == CorrectedCommand('git branch', priority=200)

    def test_remove_duplicates(self):
        side_effect = lambda *_: None
        seq = SortedCorrectedCommandsSequence(
            iter([CorrectedCommand('ls', priority=100),
                  CorrectedCommand('ls', priority=200),
                  CorrectedCommand('ls', side_effect, 300)]))
        assert set(seq) == {CorrectedCommand('ls', priority=100),
                            CorrectedCommand('ls', side_effect, 300)}

    def test_with_blank(self):
        seq = SortedCorrectedCommandsSequence(iter([]))
        assert list(seq) == []


class TestCorrectedCommand(object):

    def test_equality(self):
        assert CorrectedCommand('ls', None, 100) == \
               CorrectedCommand('ls', None, 200)
        assert CorrectedCommand('ls', None, 100) != \
               CorrectedCommand('ls', lambda *_: _, 100)

    def test_hashable(self):
        assert {CorrectedCommand('ls', None, 100),
                CorrectedCommand('ls', None, 200)} == {CorrectedCommand('ls')}
