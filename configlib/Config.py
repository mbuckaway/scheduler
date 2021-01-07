'''
Config class that loads the config file and checks it's syntax
'''
import os
import yaml
import logging
from configlib.ConfigItem import ConfigItem
from configlib.Exceptions import ConfigError

class Config:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.property_scheduleitems = []
        self.property_scheduleitemsbytime = dict()

    def ReadConfig(self, configfile: str):
        self.logger.info("Reading config from {}".format(configfile))
  
        self.filename = configfile
        configparser = None
        if not os.path.exists(configfile):
            raise FileNotFoundError(configfile)
        with open(configfile) as ymlfile:
            try:
                configparser = yaml.load(ymlfile, Loader=yaml.FullLoader)
            except Exception as e:
                raise ConfigError("Unable to parse Config file '{}': {} ".format(configfile, str(e)))
        # Parse all out items and save them to our config array and config hash
        if not type(configparser) is list:
            raise TypeError("Config file is not a list of configitems")
            
        for configdata in configparser:
            configitem = ConfigItem(configdata)
            configitem.Check()
            self.property_scheduleitems.append(configitem)
            self.property_scheduleitemsbytime[configitem.Time] = configitem


    @classmethod
    def Read(cls, filename):
        config = cls()
        config.ReadConfig(filename)
        return config

    @property
    def ConfigItems(self):
        return self.property_scheduleitems

    def GetConfigItemByTime(self, time):
        result = None
        if time in self.property_scheduleitemsbytime:
            result = self.property_scheduleitemsbytime[time]
        return result
