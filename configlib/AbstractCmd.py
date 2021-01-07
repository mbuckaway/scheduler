"""
Abstract Class that defines the layout of a command
"""

import datetime

class AbstractCmd:
    """ Base class for all commands """
    def __init__(self, config):
        self.config = config

    def Run(self, args):
        pass
