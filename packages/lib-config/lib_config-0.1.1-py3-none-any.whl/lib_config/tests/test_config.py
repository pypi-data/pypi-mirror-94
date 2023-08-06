from unittest.mock import patch


class Test_Config:
    """Tests the Config class"""

    test_config_package = "test_config"
    test_section = "Test"
    test_tags = {"a": 1, "b": 2}

    def test_write_section(self, config):
        """Writes section of config, asserts it's correct"""

        config.write_section(self.test_section, self.test_tags)
        test_lines = [f"[{self.test_section}]\n"]
        test_lines += [f"{x} = {y}\n" for x, y in self.test_tags.items()]
        test_lines += ["\n"]
        with open(config.path, "r") as f:
            assert f.readlines() == test_lines

    def test_read(self, config):
        """Reads a section from config and asserts its correct"""

        self.test_write_section(config)
        for tag, val in self.test_tags.items():
            assert config.read(self.test_section, tag=tag) == str(val)

    def test_read_no_config(self, config):
        """Reads from a config that has no section

        patches input to instead fill in section
        after which, a reread is performed
        """

        def input_patch(*args, **kwargs):
            self.test_write_section(config)
        with patch("builtins.input", input_patch):
            for tag, val in self.test_tags.items():
                assert config.read(self.test_section, tag=tag) == str(val)

    def test_get_creds(self, config):
        """Gets credits from the config file that were written"""

        self.test_write_section(config)
        vals = config.get_creds(self.test_section, tags=self.test_tags.keys())
        for key, val in zip(self.test_tags.keys(), vals):
            assert str(self.test_tags[key]) == val
