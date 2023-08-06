"""Test the show action."""
import pytest
import os
from bronotes.actions.show import ActionShow
from bronotes.config import Text
from types import SimpleNamespace
from pathlib import Path

NOTE_CONTENT = 'bladiebla'


@pytest.fixture(scope='function', params=[
    'base.md',
    'henk',
    'afewfawegawreggr',
])
def show_fixt(request, cfg_fixt):
    """Fixture for the show action class."""
    action_show = ActionShow(cfg_fixt)
    args = SimpleNamespace()
    args.note = request.param
    args.copy = False
    args.search = False
    action_show.init(args)

    if os.path.isfile(action_show.note):
        with open(action_show.note, 'w') as f:
            f.write(NOTE_CONTENT)

    return (action_show, request.param)


class TestShow():

    def test_init(self, show_fixt, dir_fixt):
        (show_fixt, arg_note) = show_fixt
        assert show_fixt.note == Path(f"{dir_fixt}/{arg_note}")

    def test_process(self, show_fixt, dir_fixt):
        (show_fixt, arg_note) = show_fixt

        result = show_fixt.process()

        if os.path.isfile(show_fixt.note):
            assert result == NOTE_CONTENT
        else:
            assert Text.E_NO_SUCH.value
