"""Окно конфигурации серверной части."""

import os
from logging import getLogger

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton,\
    QFileDialog, QApplication, QMessageBox
from configparser import ConfigParser

from common.functions import validate_port_number
from common.errors import InvalidPortNumberError
from common.constants import FILE_CONF_NAME

logger = getLogger('log_serv')


class ConfigWindow(QDialog):
    """Класс окна конфигурации параметров серверной части."""

    def __init__(self, config):
        super().__init__()
        self.config = config

        self.setFixedSize(400, 300)
        self.setWindowTitle('Настройки')
        self.setModal(True)

        self.db_path_label = QLabel('Расположение файла с базой данных:', self)
        self.db_path_label.move(15, 10)
        self.db_path_label.setFixedSize(300, 20)

        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(270, 25)
        self.db_path.move(10, 30)
        self.db_path.setReadOnly(True)

        self.choise_path_btn = QPushButton('Обзор...', self)
        self.choise_path_btn.move(290, 31)

        self.choise_path_btn.clicked.connect(self.open_file)

        self.db_name_label = QLabel('Имя файла с базой данных:', self)
        self.db_name_label.move(15, 65)

        self.db_name = QLineEdit(self)
        self.db_name.setFixedSize(150, 25)
        self.db_name.move(200, 60)

        self.port_number_label = QLabel('Номер порта для соединения:', self)
        self.port_number_label.move(15, 95)

        self.port_number = QLineEdit(self)
        self.port_number.setFixedSize(150, 25)
        self.port_number.move(200, 90)

        self.ip_address_label = QLabel(
            'С какого IP адреса\nпринимаем соединение:', self)
        self.ip_address_label.move(15, 125)

        self.ip_label_help = QLabel(
            'чтобы принимать соединения\nс любых адресов\nоставьте это поле'
            ' пустым', self)
        self.ip_label_help.move(15, 160)

        self.ip_address = QLineEdit(self)
        self.ip_address.setFixedSize(150, 25)
        self.ip_address.move(200, 125)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(180, 230)
        self.save_btn.setShortcut('Ctrl+S')

        self.close_btn = QPushButton('Закрыть', self)
        self.close_btn.move(260, 230)
        self.close_btn.setShortcut('Ctrl+Q')
        self.close_btn.clicked.connect(self.close)

        self.db_path.insert(self.config.get('Settings', 'db_path'))
        self.db_name.insert(self.config.get('Settings', 'db_file'))
        self.port_number.insert(self.config.get('Settings', 'port'))
        self.save_btn.clicked.connect(self.save_config)

        self.show()

    def open_file(self):
        """Открыть окно выбора пути."""
        dialog = QFileDialog(self)
        path = dialog.getExistingDirectory()
        path = path.replace('/', '\\')
        self.db_path.insert(path)

    def save_config(self):
        """Сохранить в файл настроек введённые параметры."""
        msg = QMessageBox()
        self.config.set('Settings', 'db_path', self.db_path.text())
        self.config.set('Settings', 'db_file', self.db_name.text())
        self.config.set('Settings', 'listen_address', self.ip_address.text())
        try:
            port_number = int(self.port_number.text())
        except ValueError:
            msg.warning(
                self,
                'Ошибка',
                'Номер порта должен быть целочисленным!')
        else:
            try:
                port_number = validate_port_number(port_number)
            except InvalidPortNumberError as e:
                msg.warning(self, 'Ошибка', str(e))
                logger.error(f'Указан некорректный номер порта: {port_number}')
                return
            else:
                self.config.set('Settings', 'port', str(port_number))
                with open(FILE_CONF_NAME, 'w') as f:
                    self.config.write(f)
                    msg.information(
                        self, 'Успех', 'Настройки успешно сохранены!')


if __name__ == '__main__':
    app = QApplication([])
    test_config = ConfigParser()
    test_file_path = os.path.join('../../', FILE_CONF_NAME)
    test_config.read(test_file_path)
    test_window = ConfigWindow(test_config)
    test_window.exec_()
