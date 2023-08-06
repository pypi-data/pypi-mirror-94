"""Test the mv action."""
import pytest
import os
from types import SimpleNamespace
from bronotes.actions.mv import ActionMove


@pytest.fixture(scope='function', params=[
    ('base.md', 'henk/'),
    ('henk/', 'henkie/'),
    ('henkie/', 'henk/henkinator/'),
])
def mv_fixt(request, cfg_fixt):
    """Fixture for the mv action class."""
    (origin, destination) = request.param
    action_mv = ActionMove(cfg_fixt)
    args = SimpleNamespace()

    args.origin = origin
    args.destination = destination
    action_mv.init(args)

    return (action_mv, origin, destination)


class TestMv():

    def test_init(self, mv_fixt, dir_fixt):
        (mv_fixt, origin, destination) = mv_fixt

        assert mv_fixt.origin == f"{dir_fixt}/{origin}"
        assert mv_fixt.destination == f"{dir_fixt}/{destination}"

    def test_process(self, mv_fixt, dir_fixt):
        (mv_fixt, origin, destination) = mv_fixt
        mv_fixt.process()

        if origin[-1] == '/':
            assert os.path.exists(dir_fixt / destination)
        else:
            assert os.path.exists(dir_fixt / destination / origin)
