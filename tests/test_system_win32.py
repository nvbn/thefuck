# -*- coding: utf-8 -*-
"""Tests for thefuck.system.win32 module.

These tests verify the Windows-specific functionality, particularly
the suppression of encoding mismatch warnings from win_unicode_console.

See: https://github.com/nvbn/thefuck/issues/514
     https://github.com/nvbn/thefuck/issues/673
"""

import warnings
import pytest

import win_unicode_console
import colorama
from thefuck.system.win32 import init_output


class TestInitOutputWarningSuppression:
    """Tests for init_output() warning suppression on Windows."""

    def test_init_output_suppresses_encoding_warning(self, mocker):
        """Test that encoding mismatch warning is suppressed."""
        def emit_encoding_warning():
            warnings.warn(
                "sys.stdin.encoding == 'utf-8', whereas sys.stdout.encoding == 'cp950', "
                "readline hook consumer may assume they are the same",
                RuntimeWarning
            )

        mock_enable = mocker.patch.object(
            win_unicode_console, 'enable',
            side_effect=emit_encoding_warning
        )
        mocker.patch.object(colorama, 'init')

        # Capture warnings during init_output call
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            init_output()

        # Verify no RuntimeWarning about encoding was propagated
        encoding_warnings = [
            w for w in caught_warnings
            if issubclass(w.category, RuntimeWarning)
            and 'stdin.encoding' in str(w.message)
        ]
        assert len(encoding_warnings) == 0, \
            "Encoding warning should be suppressed"
        mock_enable.assert_called_once()

    def test_init_output_calls_win_unicode_console_enable(self, mocker):
        """Test that win_unicode_console.enable() is called."""
        mock_enable = mocker.patch.object(win_unicode_console, 'enable')
        mocker.patch.object(colorama, 'init')

        init_output()

        mock_enable.assert_called_once()

    def test_init_output_calls_colorama_init(self, mocker):
        """Test that colorama.init() is called."""
        mocker.patch.object(win_unicode_console, 'enable')
        mock_colorama = mocker.patch.object(colorama, 'init')

        init_output()

        mock_colorama.assert_called_once()

    def test_init_output_order_win_unicode_before_colorama(self, mocker):
        """Test that win_unicode_console.enable() is called before colorama.init()."""
        call_order = []

        def record_win_unicode():
            call_order.append('win_unicode')

        def record_colorama():
            call_order.append('colorama')

        mocker.patch.object(
            win_unicode_console, 'enable',
            side_effect=record_win_unicode
        )
        mocker.patch.object(
            colorama, 'init',
            side_effect=record_colorama
        )

        init_output()

        assert call_order == ['win_unicode', 'colorama'], \
            "win_unicode_console.enable() should be called before colorama.init()"

    def test_init_output_does_not_suppress_other_warnings(self, mocker):
        """Test that other RuntimeWarnings are not suppressed."""
        def emit_other_warning():
            warnings.warn("Some other unrelated warning", RuntimeWarning)

        mocker.patch.object(
            win_unicode_console, 'enable',
            side_effect=emit_other_warning
        )
        mocker.patch.object(colorama, 'init')

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            init_output()

        # Other warnings should still be captured
        other_warnings = [
            w for w in caught_warnings
            if issubclass(w.category, RuntimeWarning)
            and 'unrelated warning' in str(w.message).lower()
        ]
        assert len(other_warnings) == 1, \
            "Other RuntimeWarnings should not be suppressed"


class TestInitOutputEncodingScenarios:
    """Tests for various encoding mismatch scenarios."""

    @pytest.mark.parametrize('stdin_enc,stdout_enc', [
        ('utf-8', 'cp950'),   # Traditional Chinese
        ('utf-8', 'cp936'),   # Simplified Chinese
        ('utf-8', 'cp1252'),  # Western European
        ('utf-8', 'cp932'),   # Japanese
        ('utf-8', 'cp949'),   # Korean
    ])
    def test_suppresses_warning_for_various_codepages(
            self, stdin_enc, stdout_enc, mocker):
        """Test warning suppression for various Windows codepage combinations."""
        def emit_warning():
            warnings.warn(
                f"sys.stdin.encoding == '{stdin_enc}', whereas "
                f"sys.stdout.encoding == '{stdout_enc}', "
                "readline hook consumer may assume they are the same",
                RuntimeWarning
            )

        mocker.patch.object(
            win_unicode_console, 'enable',
            side_effect=emit_warning
        )
        mocker.patch.object(colorama, 'init')

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            init_output()

        encoding_warnings = [
            w for w in caught_warnings
            if issubclass(w.category, RuntimeWarning)
            and 'stdin.encoding' in str(w.message)
        ]
        assert len(encoding_warnings) == 0, \
            f"Warning for {stdin_enc}/{stdout_enc} should be suppressed"
