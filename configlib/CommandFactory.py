"""
Factory class and method to return the appropriate command class based on the verb type
"""

from configlib.StartCmd import StartCmd
from configlib.StopCmd import StopCmd
from configlib.WriteCmd import WriteCmd

class CommandFactory:
    def __init__(self, configitem):
        self.configitem = configitem
        self.classswitcher = {
            'start': StartCmd,
            'stop': StopCmd,
            'write': WriteCmd,
        }

    def Command(self):
        if self.configitem.Verb == None:
            raise ValueError("invalid verb")
        result = None
        classdef = self.classswitcher.get(self.configitem.Verb.lower(), lambda: "Invalid Command")
        if classdef != None:
            result = classdef(self.configitem)
        return result
