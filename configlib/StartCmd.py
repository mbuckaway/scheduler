"""
Class for Start command
"""
import os
import subprocess
from subprocess import Popen
import shlex
import logging
import psutil
from configlib.AbstractCmd import AbstractCmd
from configlib.Exceptions import ProcessError

class StartCmd(AbstractCmd):
    def __init__(self, config):
        super(StartCmd, self).__init__(config)
        self.logger = logging.getLogger(__name__)
        self.config = config

    def Run(self):
        try:
            pid = 0
            with open(self.config.PIDFilename, mode="r") as pidfile:
                pidtext = pidfile.read()
            pid = int(pidtext)
            if psutil.pid_exists(pid):
                self.logger.warning("%s still running as PID %d, ignored", self.config.Verb, pid)
            else:
                environ = os.environ.copy()
                args = shlex.split(self.config.ProgramName)
                # If it doesn't exist, don't both running it
                if not os.path.exists(args[0]):
                    raise FileNotFoundError(args[0])
                # We assume a long running process
                ps = Popen(args, env=environ, universal_newlines=True)
                pid = ps.pid
                if pid>0:
                    with open(self.config.PIDFilename, mode="w") as pidfile:
                        pidfile.write("{}".format(pid))
        except subprocess.CalledProcessError as e:
            raise ProcessError(e.output)
        except OSError as e:
            raise ProcessError(e.strerror)
