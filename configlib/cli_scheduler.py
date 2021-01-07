import argparse
from configlib.CommandFactory import CommandFactory
import sys
import logging
import traceback
import zc.lockfile
import getpass
from configlib.Exceptions import ConfigError
from configlib.Config import Config
import datetime
import time

def scheduler():

    configfile = None

    parser = argparse.ArgumentParser(description='TVision Scheduler Tool')
    parser.add_argument('configfile', metavar="configfile", help='Config file to read')

    args = parser.parse_args()

    config = Config()
    if (args.configfile):
        configfile = args.configfile
    else:
        parser.print_help()
        sys.exit(1)

    try:
        config.ReadConfig(configfile)
    except Exception as e:
        logging.error("Config file error: %s", str(e))
        sys.exit(1)

    logging.info("Starting Scheduler with %d items", len(config.ConfigItems))

    # Main loop. Process the list of actions from the config every minute
    # Some work might have to be done to ensure items are not missed. There are some 20 different task schedulers for python
    # I chose the KISS principle due to this programming task was time boxed. This would have to be improved to be production ready.
    # Some signal handling should added so with we are asked to shut down, we do so gracefully. Not implemented due to time constraints
    while True:        # Get the time now, and see if there is an item to run
        delay = 60
        now = datetime.datetime.utcnow()
        strnow = f'{now.hour:#02d}:{now.minute:#02d}'
        logging.debug("Checking for items at %s", strnow)
        configitem = config.GetConfigItemByTime(strnow)
        if configitem:
            logging.debug("Processing %s Event", configitem.Verb)
            timestart = time.time()
            try:
                factory = CommandFactory(configitem)
                command = factory.Command()
                command.Run()
            except Exception as e:
                # Log any errors running a command
                logging.error("Cannot process %s event: %s", configitem.Verb, str(e))
            timeend = time.time()
            timerun = int(timeend - timestart)
            delay = delay - timerun
        # Wait a minute to check the time again. The amount of time to delay should include the difference between "now"
        # and the current time to make sure we never run over a interval, otherwise drifts over a second can add up
        time.sleep(delay)


def main():
    # Obviously, this is a hack for testing. Running inside a container, we are always root. But for testing,
    # allow normal users to run the program.
    lockfile = '/var/run/scheduler.lock'
    if getpass.getuser() != 'root':
        lockfile = "/tmp/scheduler.lock"

    try:
        # Config logging to go to stdout. Normally, we'd log to a file or syslog, but requirements want stdout
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        # Create a lock file so the scheduler can run once and only once
        lock = zc.lockfile.LockFile(lockfile, content_template='{pid}')
        scheduler()
        lock.close()
    except KeyboardInterrupt as e:
        logging.error("User/System requested abort")
        sys.exit(1)
    except ValueError as e:
        logging.error("Error: %s", str(e))
        sys.exit(1)
    except ConfigError as e:
        logging.error("Error reading config file: %s", str(e))
        sys.exit(1)
    except zc.lockfile.LockError as e:
        logging.critical("Error creating lockfile: scheduler already running?: %s", str(e))
        sys.exit(1)
    except Exception as e:
        logging.critical("Fatal error: {}: {}".format(str(e), traceback.format_exc()))
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
