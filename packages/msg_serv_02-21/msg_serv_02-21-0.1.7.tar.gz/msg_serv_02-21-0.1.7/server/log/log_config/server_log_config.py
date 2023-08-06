"""Файл конфигурации логирования сервера."""
import sys
import os
from logging import getLogger, handlers, Formatter, StreamHandler, DEBUG, INFO

from common.constants import DEFAULT_LOG_LEVEL, ENCODING

PATH = os.getcwd()
# PATH = os.path.join(PATH, 'log', 'logs', 'server.log')
PATH = os.path.join(PATH, 'log', 'server.log')

LOG_SERV = getLogger('log_serv')
LOG_SERV.setLevel(DEFAULT_LOG_LEVEL)

FORMATTER = Formatter(
    "%(asctime)-25s %(levelname)-10s %(module)-20s %(message)s")

FILE_HAND = handlers.TimedRotatingFileHandler(
    PATH, encoding=ENCODING, interval=1, when='midnight')
FILE_HAND.setLevel(DEBUG)

CRIT_HAND = StreamHandler(sys.stderr)
CRIT_HAND.setLevel(INFO)

FILE_HAND.setFormatter(FORMATTER)
CRIT_HAND.setFormatter(FORMATTER)

LOG_SERV.addHandler(FILE_HAND)
LOG_SERV.addHandler(CRIT_HAND)

if __name__ == '__main__':
    LOG_SERV.debug('Тестовый запуск лога сервера')
    LOG_SERV.error('Ошибка')
    LOG_SERV.info('Cообщение')
    LOG_SERV.critical('Критическая ошибка')
