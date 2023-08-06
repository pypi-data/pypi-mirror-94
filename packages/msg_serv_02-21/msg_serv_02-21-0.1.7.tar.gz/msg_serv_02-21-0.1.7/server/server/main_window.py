"""Главное окно серверной части."""

from PyQt5.Qt import QHeaderView
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, qApp, QTableView
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QTimer

from server.history_window import HistoryWindow
from server.config_window import ConfigWindow
from server.reg_user_window import RegUserWindow
from server.delete_user_window import DelUserWindow


class MainWindow(QMainWindow):
    """
    Класс - основное окно сервера. Назначает обрабочики событий, создаёт
    дочерние окна серверной части при нажатии на соответствующие кнопки,
    заполняет таблицу активных пользователей.
    """

    def __init__(self, database, server, config):
        super().__init__()
        self.database = database
        self.server = server
        self.config = config

        icon_exit = QIcon('icons/exit.png')
        self.exit_btn = QAction(icon_exit, 'Выход', self)
        self.exit_btn.setShortcut('Ctrl+Q')
        self.exit_btn.triggered.connect(qApp.quit)

        icon_update = QIcon('icons/refresh.png')
        self.update_btn = QAction(icon_update, 'Обновить список', self)

        icon_history = QIcon('icons/history.png')
        self.history_btn = QAction(icon_history, 'История пользователей', self)

        icon_config = QIcon('icons/settings.png')
        self.config_btn = QAction(icon_config, 'Настройки сервера', self)

        icon_reg_user = QIcon('icons/register.png')
        self.register_btn = QAction(icon_reg_user, 'Регистрация пользователя', self)

        icon_del_user = QIcon('icons/delete.png')
        self.delete_btn = QAction(icon_del_user, 'Удаление пользователя', self)

        self.statusBar()

        self.toolbar = self.addToolBar('Tollbar')
        self.toolbar.addAction(self.exit_btn)
        self.toolbar.addAction(self.update_btn)
        self.toolbar.addAction(self.history_btn)
        self.toolbar.addAction(self.config_btn)
        self.toolbar.addAction(self.register_btn)
        self.toolbar.addAction(self.delete_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Тестовая версия мессенджера')

        self.label = QLabel('Подключенные пользователи', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 45)

        self.users_table = QTableView(self)
        self.users_table.setFixedSize(780, 400)
        self.users_table.move(10, 65)
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.timer = QTimer()
        self.timer.timeout.connect(self.create_models)
        self.timer.start(1500)

        self.update_btn.triggered.connect(self.create_models)
        self.history_btn.triggered.connect(self.show_history)
        self.config_btn.triggered.connect(self.show_config)
        self.register_btn.triggered.connect(self.show_registration)
        self.delete_btn.triggered.connect(self.show_deletion)

        self.show()

    def create_models(self):
        """Заполнить таблицу активных пользователей."""
        users_list = self.database.get_active_users()
        lst = QStandardItemModel()
        self.users_table.setModel(lst)
        lst.setHorizontalHeaderLabels(
            ['имя', 'адрес', 'порт', 'время подключения'])

        if users_list:
            for item in users_list:
                user_name, ip, port, time = item
                user_name = QStandardItem(user_name)
                user_name.setEditable(False)
                ip = QStandardItem(ip)
                ip.setEditable(False)
                port = QStandardItem(str(port))
                port.setEditable(False)
                time = QStandardItem(str(time.replace(microsecond=0)))
                time.setEditable(False)
                lst.appendRow([user_name, ip, port, time])
            self.users_table.setModel(lst)
            self.users_table.resizeColumnsToContents()
            self.users_table.resizeRowsToContents()

    def show_history(self):
        """Показать окно истории сообщений."""
        global history_window
        history_window = HistoryWindow(self.database)

    def show_config(self):
        """Показать окно настроек сервера."""
        global config_window
        config_window = ConfigWindow(self.config)

    def show_registration(self):
        """Показать окно регистрации пользователя."""
        global reg_window
        reg_window = RegUserWindow(self.database, self.server)

    def show_deletion(self):
        """Показать окно удаления пользователя."""
        global del_window
        del_window = DelUserWindow(self.database, self.server)
