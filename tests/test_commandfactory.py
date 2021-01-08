import unittest
from configlib.ConfigItem import ConfigItem
from configlib.AbstractCmd import AbstractCmd
from configlib.StartCmd import StartCmd
from configlib.StopCmd import StopCmd
from configlib.WriteCmd import WriteCmd
from configlib.CommandFactory import CommandFactory
import logging
import time
import datetime

class TestConfigItemMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_startstop(self):
        configdata_write1 = {
            'verb': 'write',
            'time': '23:24',
            'socket_name': "/tmp/release-bunnies.sock",
            'message': "This is a test\n"
        }
        configdata_start = {
            'verb': 'start',
            'time': '23:23',
            'program_name': 'scripts/release-bunnies',
            'pidfile_name': '/tmp/release-bunnies.pid'
        }
        configdata_start2 = {
            'verb': 'start',
            'time': '23:23',
            'program_name': 'scripts/release-bunnies',
            'pidfile_name': '/tmp/release-bunnies.pid'
        }
        configdata_write = {
            'verb': 'write',
            'time': '23:24',
            'socket_name': "/tmp/release-bunnies.sock",
            'message': "This is a test\n"
        }
        configdata_stop = {
            'verb': 'stop',
            'time': '23:25',
            'program_name': 'scripts/release-bunnies',
            'pidfile_name': '/tmp/release-bunnies.pid'
        }

        configitem_write1 = ConfigItem(configdata_write1)
        self.assertTrue(configitem_write1.Check())

        configitem_start = ConfigItem(configdata_start)
        self.assertTrue(configitem_start.Check())
        
        configitem_start2 = ConfigItem(configdata_start2)
        self.assertTrue(configitem_start2.Check())

        configitem_write = ConfigItem(configdata_write)
        self.assertTrue(configitem_write.Check())

        configitem_stop = ConfigItem(configdata_stop)
        self.assertTrue(configitem_stop.Check())

        factory_write1 = CommandFactory(configitem_write1)
        command_write1 = factory_write1.Command()
        self.assertTrue(type(command_write1) is WriteCmd)

        factory_start = CommandFactory(configitem_start)
        command_start = factory_start.Command()
        self.assertTrue(type(command_start) is StartCmd)

        factory_start2 = CommandFactory(configitem_start2)
        command_start2 = factory_start2.Command()
        self.assertTrue(type(command_start2) is StartCmd)

        factory_write = CommandFactory(configitem_write)
        command_write = factory_write.Command()
        self.assertTrue(type(command_write) is WriteCmd)

        factory_stop = CommandFactory(configitem_stop)
        command_stop = factory_stop.Command()
        self.assertTrue(type(command_stop) is StopCmd)

        command_write1.Run()
        time.sleep(3)
        command_start.Run()
        time.sleep(3)
        command_start2.Run()
        time.sleep(3)
        command_write.Run()
        time.sleep(3)
        command_stop.Run()



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
