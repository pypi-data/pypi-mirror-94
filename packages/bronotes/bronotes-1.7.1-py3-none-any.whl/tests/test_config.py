class TestConfig():

    def test_cfg_values(self, cfg_fixt, dir_fixt):
        assert cfg_fixt.dir == dir_fixt
        assert not cfg_fixt.autosync
