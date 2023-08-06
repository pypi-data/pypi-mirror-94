"""Окно истории сообщений пользователей."""

from PyQt5.QtWidgets import QDialog, QPushButton, QTableView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt


class HistoryWindow(QDialog):
    """Класс окна истории сообщений пользователей."""

    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setFixedSize(600, 600)
        self.setWindowTitle('Статистика по пользователям')
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.close_btn = QPushButton('Закрыть', self)
        self.close_btn.setShortcut('Ctrl+Q')
        self.close_btn.move(250, 550)
        self.close_btn.setFixedSize(100, 30)
        self.close_btn.clicked.connect(self.close)

        self.history_table = QTableView(self)
        self.history_table.setFixedSize(500, 500)
        self.history_table.move(50, 10)

        self.create_stat_model()

        self.show()

    def create_stat_model(self):
        """Заполнить таблицу истории сообщений."""
        history_msg = self.database.get_statistics_msg()
        lst = QStandardItemModel()
        lst.setHorizontalHeaderLabels(
            ['пользователь', 'кол-во отпр. сообщ.', 'кол-во перед. сообщ.'])
        for item in history_msg:
            user_name, sent_msg_num, accepted_msg_num = item
            user_name = QStandardItem(user_name)
            user_name.setEditable(False)
            sent_msg_num = QStandardItem(str(sent_msg_num))
            sent_msg_num.setEditable(False)
            accepted_msg_num = QStandardItem(str(accepted_msg_num))
            accepted_msg_num.setEditable(False)
            lst.appendRow([user_name, sent_msg_num, accepted_msg_num])

        self.history_table.setModel(lst)
        self.history_table.resizeColumnsToContents()
        self.history_table.resizeRowsToContents()
