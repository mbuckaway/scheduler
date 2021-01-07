#
#
# Standard location for all our custom errors/exceptions

class ConfigError(RuntimeError):
    def __init__(self, message):
        self.message = message

class ProcessError(RuntimeError):
    def __init__(self, message):
        self.message = message
