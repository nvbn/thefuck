import pytest

from thefuck.rules.python_module_error import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def module_error_output(filename, module_name):
    return """Traceback (most recent call last):
  File "{0}", line 1, in <module>
    import {1}
ModuleNotFoundError: No module named '{1}'""".format(
        filename, module_name
    )


@pytest.mark.parametrize(
    "test",
    [
        Command("python hello_world.py", "Hello World"),
        Command(
            "./hello_world.py",
            """Traceback (most recent call last):
  File "hello_world.py", line 1, in <module>
    pritn("Hello World")
NameError: name 'pritn' is not defined""",
        ),
    ],
)
def test_not_match(test):
    assert not match(test)


positive_tests = [
    (
        "python some_script.py",
        "some_script.py",
        "more_itertools",
        "pip install more_itertools && python some_script.py",
    ),
    (
        "./some_other_script.py",
        "some_other_script.py",
        "a_module",
        "pip install a_module && ./some_other_script.py",
    ),
]


@pytest.mark.parametrize(
    "script, filename, module_name, corrected_script", positive_tests
)
def test_match(script, filename, module_name, corrected_script, module_error_output):
    assert match(Command(script, module_error_output))


@pytest.mark.parametrize(
    "script, filename, module_name, corrected_script", positive_tests
)
def test_get_new_command(
    script, filename, module_name, corrected_script, module_error_output
):
    assert get_new_command(Command(script, module_error_output)) == corrected_script
