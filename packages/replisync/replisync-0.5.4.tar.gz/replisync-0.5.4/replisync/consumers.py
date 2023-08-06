import json
from celery import Celery
from replisync.errors import ConfigError
import logging
logger = logging.getLogger('replisync')


class BaseConsumer(object):
    def __init__(self, conf=None):
        pass

    @classmethod
    def from_config(cls, opt):
        config = opt.get('config')
        return cls(conf=config)

    def stop(self):
        pass


class Printer(BaseConsumer):
    """
    Print the data received on stdout.
    """
    def process(self, msg):
        if isinstance(msg, str):
            logger.debug(msg)
        else:
            logger.debug(json.dumps(msg))


class CeleryConsumer(BaseConsumer):

    def __init__(self, conf=None):
        super().__init__(conf)
        broker = conf.get('replisync', 'celery_broker_url')
        if not broker:
            raise ConfigError('Celery broker not configure')

        # подключаемся к очереди задач
        self.celery_app = Celery('tasks', broker=broker)
        default_key = conf.get('replisync', 'task_default_routing_key')
        default_queue = conf.get('replisync', 'task_default_queue')
        self.celery_app.conf.task_default_routing_key = default_key
        self.celery_app.conf.task_default_queue = default_queue
        self.taskname = conf.get('replisync', 'task')
        self.system = conf.get('replisync', 'system', fallback='')

    def process(self, msg):
        changes = msg['changes']
        xid = msg['xid']

        # пихаем в очередь информацию об изменившейся записи
        if changes:
            # system - система
            # xid - транзакция
            # changes
            #   table - таблица
            #   kind - действие U, update
            #   key - ключ
            #   record - запись
            params = {
                'system': self.system,
                'xid': xid,
                'changes': changes,
            }
            logger.info('Send task "{}" with params {}'.format(
                self.taskname, params))
            self.celery_app.send_task(self.taskname, args=[], kwargs=params)
            if isinstance(changes, str):
                logger.debug(changes)
            else:
                logger.debug(json.dumps(changes))

    def stop(self):
        super().stop()

