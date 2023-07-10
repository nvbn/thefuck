import pytest


@pytest.fixture(autouse=True)
def build_container_mock(mocker):
    return mocker.patch('pytest_docker_pexpect.docker.build_container')
