'''
Config Item container class to hold information for each item in the config file and validate a config item
'''

import logging
import os
class ConfigItem:
    def __init__(self, configitem) -> None:
        self.logger = logging.getLogger(__name__)
        # Validate the item
        requiredVerbKeys = {
            "start": {
                    "time",
                    "program_name",
                    "pidfile_name"
                },
            "stop": {
                    "time",
                    "pidfile_name"
                },
            "write": {
                    "time",
                    "socket_name",
                    "message"
                }
        }
        if not 'verb' in configitem or not configitem['verb'] in requiredVerbKeys:
                raise ValueError("Missing verb or invalid verb for config item")
        
        requiredKey = requiredVerbKeys[configitem['verb']]

        # Make sure we have all the required items
        for key in requiredKey:
            if not key in configitem:
                raise ValueError("Missing key for config item: {}".format(key))
        
        # Validate the time format
        time = configitem["time"]
        if len(time) != 5:
            raise ValueError("Invalid time format for item: {}".format(configitem['verb']))
        timevals = time.split(":")
        if len(timevals) != 2:
            raise ValueError("Invalid time format for item for {}: must be HH:MM".format(configitem['verb']))
        self.property_hour = int(timevals[0])
        self.property_min = int(timevals[1])
        # Assume 24 hour format
        if self.property_hour<0 or self.property_hour>23:
            raise ValueError("Invalid hour for item for {}: must be HH:MM".format(configitem['verb']))
        if self.property_min<0 or self.property_min>59:
            raise ValueError("Invalid hour for item for {}: must be HH:MM".format(configitem['verb']))

        self.configitem = configitem
    
    def Check(self):
        result = True
        if self.IsStart and self.ProgramName and not os.path.exists(self.ProgramName):
            self.logger.warning("Program name {} does not exist!".format(self.ProgramName))
            result = False
        return result

    @property
    def Verb(self):
        return self.configitem['verb']

    @property
    def IsStart(self):
        return self.configitem['verb'] == 'start'

    @property
    def IsStop(self):
        return self.configitem['verb'] == 'stop'

    @property
    def IsWrite(self):
        return self.configitem['verb'] == 'write'

    @property
    def Hour(self):
        return self.property_hour

    @property
    def Min(self):
        return self.property_min
    
    @property
    def Time(self):
        return self.configitem['time']

    @property
    def ProgramName(self):
        result = None
        if "program_name" in self.configitem:
            result = self.configitem['program_name']
        return result

    @property
    def PIDFilename(self):
        result = None
        if "pidfile_name" in self.configitem:
            result = self.configitem['pidfile_name']
        return result

    @property
    def SocketName(self):
        result = None
        if "socket_name" in self.configitem:
            result = self.configitem['socket_name']
        return result

    @property
    def Message(self):
        result = None
        if "message" in self.configitem:
            result = self.configitem['message']
        return result
