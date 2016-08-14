from io import BytesIO

import pytest
from thefuck.rules.port_already_in_use import match, get_new_command
from tests.utils import Command

outputs = [
    '''

DE 70% 1/1 build modulesevents.js:141
      throw er; // Unhandled 'error' event
      ^

Error: listen EADDRINUSE 127.0.0.1:8080
    at Object.exports._errnoException (util.js:873:11)
    at exports._exceptionWithHostPort (util.js:896:20)
    at Server._listen2 (net.js:1250:14)
    at listen (net.js:1286:10)
    at net.js:1395:9
    at GetAddrInfoReqWrap.asyncCallback [as callback] (dns.js:64:16)
    at GetAddrInfoReqWrap.onlookup [as oncomplete] (dns.js:83:10)

    ''',
    '''
[6:40:01 AM] <START> Building Dependency Graph
[6:40:01 AM] <START> Crawling File System
 ERROR  Packager can't listen on port 8080
Most likely another process is already using this port
Run the following command to find out which process:

   lsof -n -i4TCP:8080

You can either shut down the other process:

   kill -9 <PID>

or run packager on different port.

    ''',
    '''
Traceback (most recent call last):
  File "/usr/lib/python3.5/runpy.py", line 184, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/lib/python3.5/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/home/nvbn/exp/code_view/server/code_view/main.py", line 14, in <module>
    web.run_app(app)
  File "/home/nvbn/.virtualenvs/code_view/lib/python3.5/site-packages/aiohttp/web.py", line 310, in run_app
    backlog=backlog))
  File "/usr/lib/python3.5/asyncio/base_events.py", line 373, in run_until_complete
    return future.result()
  File "/usr/lib/python3.5/asyncio/futures.py", line 274, in result
    raise self._exception
  File "/usr/lib/python3.5/asyncio/tasks.py", line 240, in _step
    result = coro.send(None)
  File "/usr/lib/python3.5/asyncio/base_events.py", line 953, in create_server
    % (sa, err.strerror.lower()))
OSError: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8080): address already in use
Task was destroyed but it is pending!
task: <Task pending coro=<RedisProtocol._reader_coroutine() running at /home/nvbn/.virtualenvs/code_view/lib/python3.5/site-packages/asyncio_redis/protocol.py:921> wait_for=<Future pending cb=[Task._wakeup()]>>
    '''
]

lsof_stdout = b'''COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
node    18233 nvbn   16u  IPv4 557134      0t0  TCP localhost:http-alt (LISTEN)
'''


@pytest.fixture(autouse=True)
def lsof(mocker):
    patch = mocker.patch('thefuck.rules.port_already_in_use.Popen')
    patch.return_value.stdout = BytesIO(lsof_stdout)
    return patch


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize(
    'command',
    [Command('./app', stdout=output) for output in outputs]
    + [Command('./app', stderr=output) for output in outputs])
def test_match(command):
    assert match(command)


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('command, lsof_output', [
    (Command('./app'), lsof_stdout),
    (Command('./app', stdout=outputs[1]), b''),
    (Command('./app', stderr=outputs[2]), b'')])
def test_not_match(lsof, command, lsof_output):
    lsof.return_value.stdout = BytesIO(lsof_output)

    assert not match(command)


@pytest.mark.parametrize(
    'command',
    [Command('./app', stdout=output) for output in outputs]
    + [Command('./app', stderr=output) for output in outputs])
def test_get_new_command(command):
    assert get_new_command(command) == 'kill 18233 && ./app'
