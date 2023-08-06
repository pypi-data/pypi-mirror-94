"""Test the edit action."""
import pytest
from pathlib import Path
from types import SimpleNamespace
from bronotes.actions.edit import ActionEdit


@pytest.fixture(scope='function', params=[
    'foo/',
    'bar.md',
    'brap/brap.md',
    'doesnt/exist/'
])
def edit_fixt(request, cfg_fixt):
    """Fixture for the list action class."""
    action_edit = ActionEdit(cfg_fixt)
    args = SimpleNamespace()
    args.file = request.param
    args.search = False
    action_edit.init(args)

    return (action_edit, request.param)


class TestEdit():

    def test_init(self, edit_fixt, dir_fixt):
        (edit_fixt, file) = edit_fixt

        assert edit_fixt.path == Path(f"{dir_fixt}/{file}")
