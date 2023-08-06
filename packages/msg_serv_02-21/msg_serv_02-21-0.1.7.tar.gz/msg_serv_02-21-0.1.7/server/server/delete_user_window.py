"""Окно удаления пользователя."""
from logging import getLogger

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton,\
    QMessageBox
from PyQt5.QtCore import Qt

LOG_SERV = getLogger('log_serv')


class DelUserWindow(QDialog):
    """Класс окна удаления пользователя."""

    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server = server
        self.message = QMessageBox()

        self.setFixedSize(300, 200)
        self.setWindowTitle('Удаление контакта')
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setModal(True)

        self.label = QLabel(
            'Выберите пользователя для удаления из контактов', self)
        self.label.move(5, 5)

        self.selector = QComboBox(self)
        self.selector.setGeometry(5, 25, 170, 20)

        self.del_btn = QPushButton('Удалить', self)
        self.del_btn.setGeometry(180, 25, 100, 30)
        self.del_btn.clicked.connect(self.delete_user)

        self.cancel_btn = QPushButton('Отмена', self)
        self.cancel_btn.setGeometry(180, 60, 100, 30)
        self.cancel_btn.clicked.connect(self.close)

        self.fill_users()
        self.show()

    def fill_users(self):
        """
        Получить всех пользователей и БД и внести их в раскрывающийся список.
        """
        contacts = self.database.get_all_users()
        self.selector.addItems(sorted(contacts))

    def delete_user(self):
        """Удалить выбранного пользвателя из БД."""
        user = self.selector.currentText()
        self.database.del_user(user)
        if user in self.server.names_to_sock:
            sock = self.server.names_to_sock[user]
            self.server.turn_sock_off(sock)
        self.server.service_update_lists(user)
        LOG_SERV.info(f'Пользователь {user} был успешно удалён.')
        self.message.information(self, 'Успех', 'Пользователь успешно удалён!')
        self.close()
