import logging
import os
import sys

from common.settings import LOGGING_LEVEL

# sys.path.append('../../')

# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.getcwd()
PATH = os.path.join(PATH, 'log/client.log')

client_log = logging.getLogger('client')
client_log.setLevel(LOGGING_LEVEL)

client_handler = logging.FileHandler(PATH, encoding='utf_8')

client_format = logging.Formatter(
    "%(asctime)-25s %(levelname)-9s %(filename)-20s %(message)s")
client_handler.setFormatter(client_format)

client_log.addHandler(client_handler)

if __name__ == '__main__':
    client_log.debug('отладочная информация')
    client_log.info('информационное сообщение')
    client_log.warning('предупреждение')
    client_log.error('ошибка')
    client_log.critical('критическая ошибка')
