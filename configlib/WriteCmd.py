"""
Class for Start command
"""
import os
import logging
import socket
from configlib.AbstractCmd import AbstractCmd

'''
WriteCmd:
Write a message to a unix socket making sure to time out before the 60 seconds
'''

class WriteCmd(AbstractCmd):
    def __init__(self, config):
        super(WriteCmd, self).__init__(config)
        self.logger = logging.getLogger(__name__)
        self.config = config

    def Run(self):
        try:
            server_address = self.config.SocketName
            # Make sure the socket exists
            if not os.path.exists(server_address):
                raise FileNotFoundError("Socket does not exist: {}".format(server_address))
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            # Ideally, the timeout would be in the config. We wait at most 15 secs to send the request
            sock.settimeout(15)
            sock.connect(server_address)
            data=self.config.Message.encode('utf8')
            sock.sendall(data)
            sock.close()
        except Exception as e:
            self.logger.error("Error sending message: {}".format(str(e)))