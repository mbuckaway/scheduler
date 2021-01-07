"""
Class for Start command
"""
import os
import psutil
import signal
import time
import logging
from configlib.AbstractCmd import AbstractCmd
from configlib.Exceptions import ProcessError

'''
StopCmd:
Open up a PID file, and send a signal to the PID
'''

class StopCmd(AbstractCmd):
    def __init__(self, config):
        super(StopCmd, self).__init__(config)
        self.logger = logging.getLogger(__name__)
        self.config = config

    def Run(self):
        if self.config.PIDFilename and os.path.exists(self.config.PIDFilename):
            pid = 0
            with open(self.config.PIDFilename, mode="r") as pidfile:
                pidtext = pidfile.read()
            pid = int(pidtext)
            if psutil.pid_exists(pid):
                ps = psutil.Process(pid)
                # Ask the process to shutdown
                ps.send_signal(signal.SIGTERM)
                time.sleep(2)
                if ps.is_running():
                    # Kill it
                    ps.kill()
            # Clean up
            os.remove(self.config.PIDFilename)
        else:
            self.logger.warning("PID file does not exist")
