import unittest
from configlib.ConfigItem import ConfigItem
import logging

class TestConfigItemMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_configitem_badverb(self):
        configitem = {
            'verb': 'test',
            'time': '23:23',
            'program_name': '/srv/release-bunnies',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        with self.assertRaises(ValueError):
            ConfigItem(configitem)

    def test_configitem_badtime(self):
        configitem = {
            'verb': 'start',
            'time': '2323',
            'program_name': '/srv/release-bunnies',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        with self.assertRaises(ValueError):
            ConfigItem(configitem)

    def test_configitem_badtime_hour(self):
        configitem = {
            'verb': 'start',
            'time': '24:23',
            'program_name': '/srv/release-bunnies',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        with self.assertRaises(ValueError):
            ConfigItem(configitem)

    def test_configitem_badtime_min(self):
        configitem = {
            'verb': 'start',
            'time': '23:60',
            'program_name': '/srv/release-bunnies',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        with self.assertRaises(ValueError):
            ConfigItem(configitem)

    def test_configitem_badtime_items(self):
        configitem = {
            'verb': 'write',
            'time': '23:00',
            'program_name': '/srv/release-bunnies',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        with self.assertRaises(ValueError):
            ConfigItem(configitem)

    def test_configitem_check_write(self):
        configitem = {
            'verb': 'write',
            'time': '23:00',
            'socket_name': '/var/run/release-bunnies.sock',
            'message': '37'
        }
        config = ConfigItem(configitem)
        self.assertTrue(config.IsWrite)
        self.assertFalse(config.IsStop)
        self.assertFalse(config.IsStart)
        self.assertEquals("23:00", config.Time)
        self.assertEquals(23, config.Hour)
        self.assertEquals(0, config.Min)
        self.assertEquals('/var/run/release-bunnies.sock', config.SocketName)
        self.assertEquals('37', config.Message)
        self.assertIsNone(config.ProgramName)
        self.assertIsNone(config.PIDFilename)

    def test_configitem_check_start(self):
        configitem = {
            'verb': 'start',
            'time': '23:01',
            'program_name': '/srv/release-bunnies',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        config = ConfigItem(configitem)
        self.assertFalse(config.IsWrite)
        self.assertFalse(config.IsStop)
        self.assertTrue(config.IsStart)
        self.assertEquals("23:01", config.Time)
        self.assertEquals(23, config.Hour)
        self.assertEquals(1, config.Min)
        self.assertEquals('/srv/release-bunnies', config.ProgramName)
        self.assertEquals('/var/run/release-bunnies.pid', config.PIDFilename)
        self.assertIsNone(config.SocketName)
        self.assertIsNone(config.Message)

    def test_configitem_check_stop(self):
        configitem = {
            'verb': 'stop',
            'time': '23:01',
            'pidfile_name': '/var/run/release-bunnies.pid'
        }
        config = ConfigItem(configitem)
        self.assertFalse(config.IsWrite)
        self.assertTrue(config.IsStop)
        self.assertFalse(config.IsStart)
        self.assertEquals("23:01", config.Time)
        self.assertEquals(23, config.Hour)
        self.assertEquals(1, config.Min)
        self.assertIsNone(config.ProgramName)
        self.assertEquals('/var/run/release-bunnies.pid', config.PIDFilename)
        self.assertIsNone(config.SocketName)
        self.assertIsNone(config.Message)


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
