#
#
# Standard location for all customer errors/exceptions

class ConfigError(RuntimeError):
    def __init__(self, message):
        self.message = message