"""Fixtures for pytest."""
import pytest
from bronotes.config import Cfg


@pytest.fixture(scope='class')
def dir_fixt(tmpdir_factory):
    """Fixture for notes directory."""
    dir_notes = tmpdir_factory.mktemp('notesdir')
    file_base = dir_notes / 'base.md'
    file_base.open(mode='w')

    dir_henk = dir_notes.mkdir('henk')
    file_blaat = dir_henk / 'henk.md'
    file_blaat.open(mode='w')
    dir_henk.mkdir('blaat')

    return dir_notes


@pytest.fixture(scope='class')
def cfg_fixt(dir_fixt, tmpdir_factory):
    """Create a config to use in tests."""
    cfg_dir = tmpdir_factory.mktemp('cfgdir')
    cfg_file = cfg_dir / 'config.yml'
    cfg_file.open(mode='w')

    cfg = Cfg()
    cfg.cfg_file = cfg_file
    cfg.dict = {}
    cfg.set_dir(dir_fixt)
    cfg.init()

    return cfg
