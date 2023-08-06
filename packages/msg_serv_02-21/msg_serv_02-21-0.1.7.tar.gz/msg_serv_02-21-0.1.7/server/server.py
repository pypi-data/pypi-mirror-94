"""Скрипт запуска сервера."""

import os
import sys
from logging import getLogger

from threading import Lock

from PyQt5.QtWidgets import QApplication
from configparser import ConfigParser

from server.main_window import MainWindow
from server.create_conf_file import Config
from server.core import HandlerMessage
from common.constants import FILE_CONF_NAME
from common.errors import MissingArgumentParser
from server.server_database import HandlerServDB
from log.log_config import server_log_config

LOG_SERV = getLogger('log_serv')

flag_lock = Lock()


def get_param(default_port, default_address):
    """
    Получить параметры из командной строки.
    Значения параметров по умолчанию:
    адрес хоста: 127.0.0.1
    порт: 8888
    :return:
    """
    parser = MissingArgumentParser()
    parser.add_argument('-a', '--address', default=default_address, nargs='?')
    parser.add_argument('-p', '--port', default=default_port, type=int, nargs='?')
    parser.add_argument('--no_gui', action='store_false')
    args = parser.parse_args()
    serv_port = args.port
    serv_host = args.address
    gui_flag = args.no_gui

    return serv_host, serv_port, gui_flag


def main():
    """Запустить в работу серверную часть."""
    conf = config_load()
    serv_host, serv_port, gui_flag = get_param(conf.get('Settings', 'port'), conf.get('Settings', 'listen_address'))
    a = conf.get('Settings', 'db_file')
    database = HandlerServDB(a)
    serv = HandlerMessage(serv_host, serv_port, database)
    serv.daemon = True
    serv.start()

    if gui_flag:
        server_app = QApplication(sys.argv)
        main_window = MainWindow(database, serv, conf)
        server_app.exec_()
        serv.running = False
    else:
        while True:
            command = input('Введите e для завершения работы сервера: ')
            if command == 'e':
                serv.running = False
                break


def config_load():
    """Загрузить сохраненные параметры конфигурации."""
    conf = ConfigParser()
    file_conf_path = os.path.join(os.getcwd(), FILE_CONF_NAME)
    conf.read(file_conf_path)
    if 'Settings' in conf:
        return conf
    else:
        conf_obj = Config()
        conf_obj.create_config()
        return conf_obj


if __name__ == '__main__':
    main()





