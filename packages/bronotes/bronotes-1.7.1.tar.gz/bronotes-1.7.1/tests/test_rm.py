"""Test the rm action."""
import pytest
from pathlib import Path
import os
from types import SimpleNamespace
from bronotes.actions.rm import ActionDel
from bronotes.config import Text


@pytest.fixture(scope='function', params=[
    'base.md',
    'henk',
    'henk/henk.md',
    'bladiebladoesntexist'
])
def rm_fixt(request, cfg_fixt):
    """Fixture for the rm action class."""
    argument = request.param
    action_rm = ActionDel(cfg_fixt)
    args = SimpleNamespace()

    args.argument = argument
    args.recurse = False
    action_rm.init(args)

    return (action_rm, argument)


class TestRm():

    def test_init(self, rm_fixt, dir_fixt):
        (rm_fixt, argument) = rm_fixt

        assert rm_fixt.path == Path(f"{dir_fixt}/{argument}")

    def test_process(self, rm_fixt, dir_fixt):
        (rm_fixt, argument) = rm_fixt
        result = rm_fixt.process()

        assert (not os.path.exists(rm_fixt.path)
                or result == Text.E_DIR_NOT_EMPTY.value)

    def test_recurse(self, rm_fixt, dir_fixt):
        (rm_fixt, argument) = rm_fixt
        rm_fixt.recurse = True
        rm_fixt.process()

        assert not os.path.exists(rm_fixt.path)
