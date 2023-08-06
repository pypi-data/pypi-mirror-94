"""Test the add action."""
import os
import pytest
from pathlib import Path
from types import SimpleNamespace
from bronotes.actions.add import ActionAdd
from bronotes.config import Text


@pytest.fixture(scope='function', params=[
    'foo/',
    'foo/',
    'bar.md',
    'brap/brap.md',
    'doesnt/exist/'
])
def add_fixt(request, cfg_fixt):
    """Fixture for the list action class."""
    action_add = ActionAdd(cfg_fixt)
    args = SimpleNamespace()
    args.argument = request.param
    args.recurse = True
    action_add.init(args)

    return (action_add, request.param)


class TestAdd():

    def test_init(self, add_fixt, dir_fixt):
        (add_fixt, argument) = add_fixt

        if argument == '':
            assert not add_fixt.path
        else:
            assert add_fixt.path == Path(f"{dir_fixt}/{argument}")

    def test_process(self, add_fixt, dir_fixt):
        (add_fixt, argument) = add_fixt
        result = add_fixt.process()

        assert (os.path.exists(dir_fixt / argument)
                or result == Text.E_FILE_NOT_FOUND.value)

        if argument[-1] == '/':
            assert os.path.isdir(dir_fixt / argument)
        else:
            assert os.path.isfile(dir_fixt / argument)

    def test_recurse(self, add_fixt, dir_fixt):
        (add_fixt, argument) = add_fixt
        add_fixt.recurse = True
        add_fixt.process()

        assert os.path.exists(dir_fixt / argument)
