import pytest

from pytest_docker_pexpect.docker import run as pexpect_docker_run, \
    stats as pexpect_docker_stats


@pytest.fixture(autouse=True)
def build_container_mock(mocker):
    return mocker.patch('pytest_docker_pexpect.docker.build_container')


def run_side_effect(*args, **kwargs):
    container_id = pexpect_docker_run(*args, **kwargs)
    pexpect_docker_stats(container_id)
    return container_id


@pytest.fixture(autouse=True)
def run_mock(mocker):
    return mocker.patch('pytest_docker_pexpect.docker.run', side_effect=run_side_effect)
