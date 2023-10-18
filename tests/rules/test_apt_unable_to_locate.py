from io import BytesIO

import pytest
from thefuck.rules.apt_unable_to_locate import (
    match,
    get_new_command,
    _get_search_results,
)
from thefuck.types import Command

invalid_operation = "E: Unable to locate package {}".format
apt_rabbitmq_search_results = b""" kamailio-rabbitmq-modules/bionic 5.1.2-1ubuntu2 amd64
  RabbitMQ and AMQP integration modules for the Kamailio SIP server

libanyevent-rabbitmq-perl/bionic 1.19+dfsg-1 all
  asynchronous and multi channel Perl AMQP client

libmojo-rabbitmq-client-perl/bionic 0.1.0-1 all
  Mojo::IOLoop based RabbitMQ client

libmono-messaging-rabbitmq4.0-cil/bionic 4.6.2.7+dfsg-1ubuntu1 all
  Mono Messaging RabbitMQ library (for CLI 4.0)

libmono-rabbitmq4.0-cil/bionic 4.6.2.7+dfsg-1ubuntu1 all
  Mono RabbitMQ.Client library (for CLI 4.0)

librabbitmq-client-java/bionic 5.0.0-1 all
  RabbitMQ Java client

librabbitmq-dbg/bionic-updates,bionic-security 0.8.0-1ubuntu0.18.04.2 amd64
  AMQP client library written in C - Debug Files

librabbitmq-dev/bionic-updates,bionic-security 0.8.0-1ubuntu0.18.04.2 amd64
  AMQP client library written in C - Dev Files

librabbitmq4/bionic-updates,bionic-security 0.8.0-1ubuntu0.18.04.2 amd64
  AMQP client library written in C

nagios-plugins-rabbitmq/bionic-updates 1:1.2.0-2.2ubuntu0.18.04.1 all
  Set of Nagios checks useful for monitoring a RabbitMQ server

opensips-rabbitmq-module/bionic 2.2.2-3build4 amd64
  Interface module to interact with a RabbitMQ server

puppet-module-puppetlabs-rabbitmq/bionic 5.3.1-2 all
  Puppet module for rabbitmq, manage everything from vhosts to exchanges

rabbitmq-server/bionic 3.6.10-1 all
  AMQP server written in Erlang

"""
apt_get_rabbitmq_search_results = b"""
kamailio-rabbitmq-modules - RabbitMQ and AMQP integration modules for the Kamailio SIP server
libanyevent-rabbitmq-perl - asynchronous and multi channel Perl AMQP client
libmojo-rabbitmq-client-perl - Mojo::IOLoop based RabbitMQ client
libmono-messaging-rabbitmq4.0-cil - Mono Messaging RabbitMQ library (for CLI 4.0)
libmono-rabbitmq4.0-cil - Mono RabbitMQ.Client library (for CLI 4.0)
librabbitmq-client-java - RabbitMQ Java client
librabbitmq-dbg - AMQP client library written in C - Debug Files
librabbitmq-dev - AMQP client library written in C - Dev Files
librabbitmq4 - AMQP client library written in C
nagios-plugins-rabbitmq - Set of Nagios checks useful for monitoring a RabbitMQ server
opensips-rabbitmq-module - Interface module to interact with a RabbitMQ server
puppet-module-puppetlabs-rabbitmq - Puppet module for rabbitmq, manage everything from vhosts to exchanges
rabbitmq-server - AMQP server written in Erlang
"""
rabbitmq_search_search_results = [
    "kamailio-rabbitmq-modules",
    "libanyevent-rabbitmq-perl",
    "libmojo-rabbitmq-client-perl",
    "libmono-messaging-rabbitmq4.0-cil",
    "libmono-rabbitmq4.0-cil",
    "librabbitmq-client-java",
    "librabbitmq-dbg",
    "librabbitmq-dev",
    "librabbitmq4",
    "nagios-plugins-rabbitmq",
    "opensips-rabbitmq-module",
    "puppet-module-puppetlabs-rabbitmq",
    "rabbitmq-server",
]


@pytest.mark.parametrize(
    "command",
    [
        (Command("apt install rabbitmq", invalid_operation("rabbitmq"))),
        (Command("apt-get install rabbitmq", invalid_operation("rabbitmq"))),
    ],
)
def test_match(command):
    assert match(command)


@pytest.mark.parametrize(
    "command",
    [
        (Command("yarn install reactjs", "a_bad_cmd: command not found")),
        (Command("npm install reactjs", "a_bad_cmd: command not found")),
        (Command("apt upgrade", "a_bad_cmd: command not found")),
    ],
)
def test_not_match(command):
    assert not match(command)


@pytest.fixture
def set_search(mocker):
    mock = mocker.patch("subprocess.Popen")

    def _set_text(text):
        mock.return_value.stdout = BytesIO(text)

    return _set_text


@pytest.mark.parametrize(
    "app, command, search_text, search_results",
    [
        (
            "apt",
            "rabbitmq",
            apt_rabbitmq_search_results,
            rabbitmq_search_search_results,
        ),
        (
            "apt-get",
            "rabbitmq",
            apt_get_rabbitmq_search_results,
            rabbitmq_search_search_results,
        ),
    ],
)
def test_get_search_results(set_search, app, command, search_text, search_results):
    set_search(search_text)
    assert _get_search_results(app, command) == search_results


@pytest.mark.parametrize(
    "command, expected_command, search_text",
    [
        (
            Command("sudo apt install rabbitmq", invalid_operation("rabbitmq")),
            [
                "sudo apt install librabbitmq4",
                "sudo apt install rabbitmq-server",
                "sudo apt install librabbitmq-dev",
            ],
            apt_rabbitmq_search_results,
        )
    ],
)
def test_get_new_command(set_search, command, expected_command, search_text):
    set_search(search_text)
    assert get_new_command(command) == expected_command
