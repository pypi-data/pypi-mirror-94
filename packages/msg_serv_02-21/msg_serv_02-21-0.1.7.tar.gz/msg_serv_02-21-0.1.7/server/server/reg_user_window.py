"""Окно регистрации пользователя."""

import hashlib
import binascii
from logging import getLogger

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton,\
    QApplication, QMessageBox
from PyQt5.QtCore import Qt

LOG_SERV = getLogger('log_serv')


class RegUserWindow(QDialog):
    """Класс окна регистрации пользователя."""

    def __init__(self, database, server):
        super().__init__()
        self.message = QMessageBox()
        self.database = database
        self.server = server

        self.setFixedSize(200, 200)
        self.setWindowTitle('Добавление пользователя')
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setModal(True)

        self.label_name = QLabel('Введите имя пользователя:', self)
        self.label_name.move(5, 10)

        self.user_name = QLineEdit(self)
        self.user_name.setGeometry(5, 25, 190, 25)

        self.label_password = QLabel('Введите пароль:', self)
        self.label_password.move(5, 55)

        self.password = QLineEdit(self)
        self.password.setGeometry(5, 70, 190, 25)
        self.password.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.label_repeat_psw = QLabel('Повторите пароль:', self)
        self.label_repeat_psw.move(5, 100)

        self.repeat_psw = QLineEdit(self)
        self.repeat_psw.setGeometry(5, 115, 190, 25)
        self.repeat_psw.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.setGeometry(5, 160, 92, 25)
        self.save_btn.clicked.connect(self.save_user)

        self.exit_btn = QPushButton('Выход', self)
        self.exit_btn.setGeometry(100, 160, 92, 25)
        self.exit_btn.clicked.connect(self.close)

        self.show()

    def save_user(self):
        """Сделать проверку заполненных полей ввода и если всё верно
        захешировать пароль и сохранить пользователя в БД."""
        user_name = self.user_name.text()
        password = self.password.text()
        repeat_psw = self.repeat_psw.text()
        if not user_name:
            self.message.warning(self, 'Ошибка', 'Введите имя пользователя!')
        elif not password:
            self.message.warning(self, 'Ошибка', 'Введите пароль!')
        elif not repeat_psw:
            self.message.warning(self, 'Ошибка', 'Повторите пароль!')
        elif password != repeat_psw:
            self.message.warning(
                self, 'Ошибка', 'Введённые пароли не совпадают!')
        elif self.database.check_user(user_name):
            self.message.warning(
                self, 'Ошибка', 'Пользователь с таким именем уже существет!')
        else:
            passw_bytes = password.encode('utf-8')
            salt_bytes = user_name.upper().encode('utf-8')
            passw_hash = hashlib.pbkdf2_hmac(
                'sha256', passw_bytes, salt_bytes, 100000)
            self.database.create_user(user_name, binascii.hexlify(passw_hash))
            LOG_SERV.info(
                f'Пользователь {user_name} был успешно зарегистрирован.')
            self.message.information(
                self, 'Успех', 'Пользователь успешно зарегистрирован!')
            self.server.service_update_lists(user_name)
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = RegUserWindow(None, None)
    window.show()
    app.exec_()
