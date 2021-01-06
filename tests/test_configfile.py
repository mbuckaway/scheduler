import unittest
from configlib.ConfigItem import ConfigItem
from configlib.Config import Config
import logging

class TestConfigItemMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_configfile_doesnotexist(self):
        with self.assertRaises(FileNotFoundError):
            Config.Read("bad.yaml")


    def test_configfile_load_bad(self):
        with self.assertRaises(TypeError):
            Config.Read("tests/test_config_bad.yaml")

    def test_configfile_load(self):
        config = Config.Read("config.yaml")
        self.assertEquals(3, len(config.ConfigItems))
        self.assertIsNotNone(config.GetConfigItemByTime("11:30"))
        self.assertIsNotNone(config.GetConfigItemByTime("13:30"))
        self.assertIsNotNone(config.GetConfigItemByTime("12:30"))
        self.assertTrue(config.GetConfigItemByTime("11:30"))
        self.assertTrue(config.GetConfigItemByTime("13:30"))
        self.assertTrue(config.GetConfigItemByTime("12:30"))


if __name__ == '__main__':
    root_logger = logging.getLogger('')
    # Setup logging to the screen
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] [%(name)-15.15s] [%(levelname)-7.7s] %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to logger
    root_logger.addHandler(ch)
    unittest.main()
