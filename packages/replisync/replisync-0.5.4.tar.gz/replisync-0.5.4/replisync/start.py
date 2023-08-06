import sys, os
from replisync.errors import ReplisyncError, ConfigError
from replisync.config import make_pipeline, parse_config

import logging
logger = logging.getLogger('replisync')


def main():
    opt = parse_cmdline()
    logging.basicConfig(
        level=opt.loglevel,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    # файл конфига либо передается параметром, либо из окружения
    configfile = opt.configfile or os.getenv('REPLISYNC_CONF')

    if configfile:
        conf = parse_config(configfile)
    else:
        raise ConfigError("No config file")

    logfile = conf.get('replisync', 'logfile', fallback=None) or opt.logfile
    if logfile:
        fh = logging.FileHandler(logfile)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    pl = make_pipeline(conf, dsn=opt.dsn, slot=opt.slot)
    pl.start(slot_create=opt.slot_create, lsn=opt.lsn)


def parse_cmdline():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('configfile', nargs='?',
                        help="configuration file to parse; if not specified "
                             "print on stderr")

    parser.add_argument('--dsn',
                        help="database to read from (override config file)")
    parser.add_argument('--slot',
                        help="the replication slot to connect to (override "
                             "config file)")
    parser.add_argument('--slot-create',
                        action='store_true',
                        help='creates the named replication slot')
    parser.add_argument('--lsn', default='0/0',
                        help="the replication starting point [default: "
                             "%(default)s]")

    g = parser.add_mutually_exclusive_group()
    g.add_argument('-v', '--verbose', dest='loglevel',
        action='store_const', const=logging.DEBUG, default=logging.INFO,
        help="print debugging information to stderr")
    g.add_argument('-q', '--quiet', dest='loglevel',
        action='store_const', const=logging.WARN,
        help="minimal output on stderr")
    g.add_argument('--logfile', dest='logfile', help="log file name")

    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    try:
        sys.exit(main())

    except ReplisyncError as e:
        logger.error("%s", e)
        sys.exit(1)

    except Exception:
        logger.exception("unexpected error")
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("user interrupt")
        sys.exit(1)