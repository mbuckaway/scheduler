import argparse
import sys
import logging
import traceback
import zc.lockfile
import getpass
from configlib.Exceptions import ConfigError
from configlib.Config import Config


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
