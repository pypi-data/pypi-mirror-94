import sys
import configparser
from replisync.errors import ConfigError
from replisync.pipeline import Pipeline
import logging
logger = logging.getLogger('replisync')


DEFAULT_CONFIG = {
    # Настройка основной базы данных
    # --------------------------------------------------------------------------
    'database': {
        'DATABASE_ENGINE': 'django.db.backends.postgresql_psycopg2',
        'DATABASE_NAME': 'bars_web_bb',
        'DATABASE_USER': 'bars_web_bb',
        'DATABASE_PASSWORD': 'bars_web_bb',
        'DATABASE_HOST': '127.0.0.1',
        'DATABASE_PORT': '5432',
    },
    'replisync': {
        'plugin': 'replisome',
        'slot': 'selfrepl',
        'receiver': 'JsonReceiver',
        'consumer': 'Printer',
        'pretty-print': True,
        'dsn': '',
        'task': 'replisync',
        'include_xids': True,
        'include_timestamp': True,
        'task_default_routing_key': 'replisync',
        'task_default_queue': 'replisync',
    },
}

REPLISYNC_KEYS = [
    'plugin', 'slot', 'receiver', 'consumer', 'dsn', 'task',
    'celery_broker_url', 'system', 'logfile',
    'database_engine', 'database_name', 'database_user',
    'database_password', 'database_host', 'database_port',
    'task_default_routing_key', 'task_default_queue',
]


def parse_config(filename):
    if filename == '-':
        return parse_file(sys.stdin)
    else:
        try:
            with open(filename) as f:
                return parse_file(f)
        except IOError as e:
            raise ConfigError(e)


def parse_file(f):
    try:
        conf = configparser.ConfigParser()
        conf.read_dict(DEFAULT_CONFIG)
        conf.read_file(f)
        return conf
    except Exception as e:
        raise ConfigError("bad config file: %s" % e)


def dsn_from_database(conf):
    dsn = conf.get('replisync', 'dsn', fallback=None)
    return dsn or 'postgresql://{0}{1}@{2}{3}/{4}'.format(
        conf.get('database', 'DATABASE_USER'),
        conf.get('database', 'DATABASE_PASSWORD'),
        conf.get('database', 'DATABASE_HOST'),
        conf.get('database', 'DATABASE_PORT'),
        conf.get('database', 'DATABASE_NAME'),
    )


def make_pipeline(config, dsn=None, slot=None):
    pl = Pipeline()
    if not dsn:
        dsn = dsn_from_database(config)

    recv_opt = [(k, v) for k, v in config.items('replisync')
                if k not in REPLISYNC_KEYS]
    recv = {
        'class': config.get('replisync', 'receiver'),
        'options': dict(recv_opt),
        'slot': slot or config.get('replisync', 'slot'),
        'plugin': config.get('replisync', 'plugin'),
    }
    logger.debug('Receiver params: {}'.format(recv))
    pl.receiver = make_receiver(recv, dsn=dsn, slot=slot)
    cons = {
        'class': config.get('replisync', 'consumer'),
        'options': {'config': config},
    }
    logger.debug('Consumer params: {}'.format(cons))
    pl.consumer = make_consumer(cons)
    return pl


def make_receiver(config, dsn=None, slot=None):
    try:
        obj = make_object(config, package='replisync.receivers')
    except ConfigError as e:
        raise ConfigError("bad receiver configuration: %s" % e)

    if dsn is not None:
        obj.dsn = dsn
    else:
        try:
            obj.dsn = config.pop('dsn')
        except KeyError:
            raise ConfigError("no receiver dsn specified")

    if slot is not None:
        obj.slot = slot
    else:
        try:
            obj.slot = config.pop('slot')
        except KeyError:
            raise ConfigError("no receiver slot specified")

    obj.plugin = config.pop('plugin', 'replisome')

    if config:
        raise ConfigError(
            "unknown receiver configuration entries: %s" %
            ', '.join(sorted(config)))

    return obj


def make_consumer(config):
    try:
        obj = make_object(config, package='replisync.consumers')
    except ConfigError as e:
        raise ConfigError("bad consumer configuration: %s" % e)
    return obj


def deep_import(name):
    pkgname, objname = name.rsplit('.', 1)
    m = __import__(pkgname, fromlist=[objname])
    return getattr(m, objname)


def make_object(config, package=None):
    if not isinstance(config, dict):
        raise ConfigError("config should be an object")

    try:
        cls = config.pop('class')
    except KeyError:
        raise ConfigError("no class specified")

    options = config.pop('options', {})

    if not isinstance(options, dict):
        raise ConfigError("options should be an object")

    if package and '.' not in cls:
        cls = "%s.%s" % (package, cls)

    try:
        cls = deep_import(cls)
    except ImportError as e:
        raise ConfigError("error importing class: %s: %s" % (cls, e))

    if not isinstance(cls, type):
        raise ConfigError("not a type: %s" % (cls,))

    if hasattr(cls, 'from_config'):
        return cls.from_config(options)
    else:
        return cls(**options)
