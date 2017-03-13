import pytest
from mock import MagicMock
from thefuck.shells.generic import ShellConfiguration
from thefuck.not_configured import main


@pytest.fixture(autouse=True)
def usage_tracker(mocker):
    return mocker.patch(
        'thefuck.not_configured._get_not_configured_usage_tracker_path',
        new_callable=MagicMock)


def _assert_tracker_updated(usage_tracker, pid):
    usage_tracker.return_value \
        .open.return_value \
        .__enter__.return_value \
        .write.assert_called_once_with(str(pid))


def _change_tracker(usage_tracker, pid):
    usage_tracker.return_value.exists.return_value = True
    usage_tracker.return_value \
        .open.return_value \
        .__enter__.return_value \
        .read.return_value = str(pid)


@pytest.fixture(autouse=True)
def shell_pid(mocker):
    return mocker.patch('thefuck.not_configured._get_shell_pid',
                        new_callable=MagicMock)


@pytest.fixture(autouse=True)
def shell(mocker):
    shell = mocker.patch('thefuck.not_configured.shell',
                         new_callable=MagicMock)
    shell.get_history.return_value = []
    shell.how_to_configure.return_value = ShellConfiguration(
        content='eval $(thefuck --alias)',
        path='/tmp/.bashrc',
        reload='bash',
        can_configure_automatically=True)
    return shell


@pytest.fixture(autouse=True)
def shell_config(mocker):
    path_mock = mocker.patch('thefuck.not_configured.Path',
                             new_callable=MagicMock)
    return path_mock.return_value \
        .expanduser.return_value \
        .open.return_value \
        .__enter__.return_value


@pytest.fixture(autouse=True)
def logs(mocker):
    return mocker.patch('thefuck.not_configured.logs',
                        new_callable=MagicMock)


def test_for_generic_shell(shell, logs):
    shell.how_to_configure.return_value = None
    main()
    logs.how_to_configure_alias.assert_called_once()


def test_on_first_run(usage_tracker, shell_pid, logs):
    shell_pid.return_value = 12
    usage_tracker.return_value.exists.return_value = False
    main()
    _assert_tracker_updated(usage_tracker, 12)
    logs.how_to_configure_alias.assert_called_once()


def test_on_run_after_other_commands(usage_tracker, shell_pid, shell, logs):
    shell_pid.return_value = 12
    shell.get_history.return_value = ['fuck', 'ls']
    _change_tracker(usage_tracker, 12)
    main()
    logs.how_to_configure_alias.assert_called_once()


def test_on_first_run_from_current_shell(usage_tracker, shell_pid,
                                         shell, logs):
    shell.get_history.return_value = ['fuck']
    shell_pid.return_value = 12
    _change_tracker(usage_tracker, 55)
    main()
    _assert_tracker_updated(usage_tracker, 12)
    logs.how_to_configure_alias.assert_called_once()


def test_when_cant_configure_automatically(shell_pid, shell, logs):
    shell_pid.return_value = 12
    shell.how_to_configure.return_value = ShellConfiguration(
        content='eval $(thefuck --alias)',
        path='/tmp/.bashrc',
        reload='bash',
        can_configure_automatically=False)
    main()
    logs.how_to_configure_alias.assert_called_once()


def test_when_already_configured(usage_tracker, shell_pid,
                                 shell, shell_config, logs):
    shell.get_history.return_value = ['fuck']
    shell_pid.return_value = 12
    _change_tracker(usage_tracker, 12)
    shell_config.read.return_value = 'eval $(thefuck --alias)'
    main()
    logs.already_configured.assert_called_once()


def test_when_successfuly_configured(usage_tracker, shell_pid,
                                     shell, shell_config, logs):
    shell.get_history.return_value = ['fuck']
    shell_pid.return_value = 12
    _change_tracker(usage_tracker, 12)
    shell_config.read.return_value = ''
    main()
    shell_config.write.assert_any_call('eval $(thefuck --alias)')
    logs.configured_successfully.assert_called_once()
