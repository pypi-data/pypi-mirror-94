"""Test the list action."""
import pytest
from bronotes.actions.list import Tree
from bronotes.actions.list import ActionList
from bronotes.config import Text
from types import SimpleNamespace
from pathlib import Path


@pytest.fixture(scope='function', params=[
    'henk',
    '',
    'absent',
])
def list_fixt(request, cfg_fixt):
    """Fixture for the list action class."""
    action_list = ActionList(cfg_fixt)
    args = SimpleNamespace()
    args.dir = request.param
    args.directories = False
    action_list.init(args)

    return (action_list, request.param)


class TestList():

    def test_init(self, list_fixt, dir_fixt):
        (list_fixt, arg_dir) = list_fixt
        assert list_fixt.path == Path(f"{dir_fixt}/{arg_dir}")

    def test_process(self, list_fixt, dir_fixt):
        (list_fixt, arg_dir) = list_fixt

        if arg_dir == 'absent':
            assert list_fixt.process() == Text.I_NO_DIR.value
        else:
            assert str(list_fixt.process()) == str(Tree(list_fixt.path))
