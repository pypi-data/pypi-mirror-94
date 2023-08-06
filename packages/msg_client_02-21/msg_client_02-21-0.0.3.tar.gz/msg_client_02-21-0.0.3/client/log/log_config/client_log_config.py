"""Файл конфигурации логирования клиента."""
import sys
import os
from logging import getLogger, handlers, Formatter, StreamHandler, DEBUG, INFO

from common.constants import DEFAULT_LOG_LEVEL

PATH = os.getcwd()
# PATH = os.path.join(PATH, 'log', 'logs', 'client.log')
PATH = os.path.join(PATH, 'log', 'client.log')

LOG_CLIENT = getLogger('log_client')
LOG_CLIENT.setLevel(DEFAULT_LOG_LEVEL)

FORMATTER = Formatter(
    "%(asctime)-25s %(levelname)-10s %(module)-20s %(message)s")

FILE_HAND = handlers.RotatingFileHandler(
    PATH, maxBytes=500000, encoding='utf-8')
FILE_HAND.setLevel(DEBUG)

CRIT_HAND = StreamHandler(sys.stderr)
CRIT_HAND.setLevel(INFO)

FILE_HAND.setFormatter(FORMATTER)
CRIT_HAND.setFormatter(FORMATTER)

LOG_CLIENT.addHandler(FILE_HAND)
LOG_CLIENT.addHandler(CRIT_HAND)

if __name__ == '__main__':
    LOG_CLIENT.debug('Тестовый запуск лога клиента')
    LOG_CLIENT.error('Ошибка')
    LOG_CLIENT.info('Cообщение')
    LOG_CLIENT.critical('Критическая ошибка')
