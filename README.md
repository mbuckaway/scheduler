# Sample Python Scheduler

This is an example of a scheduler written in Python. It reads a config file, starts and stops processes, and writes data to a UNIX socket. The code has been tested on Python 3.9 on Mac OSX and Ubuntu Linux 20.20.

## Config File Format

Config file is a YAML formatted file. It supports only a list of items. All other items are not permitted. If the yaml file is not a list, the program will refuse to start.

'''
- time: "23:49"
  verb: "start"
  program_name: "scripts/release-bunnies"
  pidfile_name: "/tmp/release-bunnies.pid"
- time: "23:50"
  verb: "write"
  socket_name: "/tmp/release-bunnies.sock"
  message: "37" 
- time: "23:51"
  verb: "stop"
  pidfile_name: "/tmp/release-bunnies.pid"
'''

Three types of commands are supported:
* start - starts a program, if not already running, and creates a PID file
* stop - stops a running program
* write - writes a message to a unix socket. There is a 15 second timeout in case the socket blocks.


## Running the app

Usage:

'''bash
scheduler configfilename.yaml
'''

The program takes one argument and that is the config file. '-h' will return help text. A sample config file, config.yaml, has been provided.

## Installing

The code by itself will run out of the box with the "scheduler" command line utility. The 'scripts/release-bunnies' program exists for testing. This script requires netcat to be installed to act as a server. We could have written a python utility, but if was faster to create a shell script considering the reason for the program. This method requires pip to install the requirements:

'''
pip3 install -r requirements
scheduler config.yaml
'''




Alternatively, a setup.py has been provided. To use this method, for testing purposes, create a virtual environment first:
'''
python3 -m venv env
. env/bin/activate
python3 setup.py install
scheduler config.yaml
