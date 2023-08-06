"""Создание файла конфигурации."""

import os
from configparser import ConfigParser

from common.constants import FILE_CONF_NAME, SERV_DB_NAME, DEFAULT_PORT


class Config(ConfigParser):
    """Класс для создания файла конфигурации."""
    def __init__(self):
        super().__init__()

    def create_config(self):
        """Создать файл конфигурации."""
        file_conf_path = os.path.join(os.getcwd(), FILE_CONF_NAME)
        self.add_section("Settings")
        self.set("Settings", "db_path", "")
        self.set("Settings", "db_file", SERV_DB_NAME)
        self.set("Settings", "port", str(DEFAULT_PORT))
        self.set("Settings", "listen_address", "")

        with open(file_conf_path, "w", encoding='utf-8') as f:
            self.write(f)


if __name__ == "__main__":
    print(os.path.split(os.getcwd())[0])
    conf_obj = Config()
    conf_obj.create_config()
