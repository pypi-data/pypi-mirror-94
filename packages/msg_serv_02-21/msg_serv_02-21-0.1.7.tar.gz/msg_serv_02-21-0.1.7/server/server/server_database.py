"""БД сервера."""
import datetime
from logging import getLogger
from tabulate import tabulate

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, DateTime, Text, ForeignKey, exc
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator

from common.constants import SERV_DB_NAME

LOG_SERV = getLogger('log_serv')


class HandlerServDB:
    """
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """

    class Users:
        """Класс таблицы всех пользователей."""

        def __init__(self, name, date_register, psw_hash):
            self.id = None
            self.name = name
            self.date_register = date_register
            self.psw_hash = psw_hash
            self.pubkey = None

        def __str__(self):
            return f'the user {self.name}'

    class ActiveUsers:
        """Класс таблицы пользователей подключенных в данный момент времени."""

        def __init__(self, user_id, ip_address, port, date_login):
            self.id = None
            self.user_id = user_id
            self.ip_address = ip_address
            self.port = port
            self.date_login = date_login

        def __str__(self):
            return f'the user {self.user_id} is active'

    class Messages:
        """Класс таблицы сообщений пользователей."""

        def __init__(self, sender, recipient, text_message, send_date):
            self.id = None
            self.sender = sender
            self.recipient = recipient
            self.text_message = text_message
            self.send_date = send_date

        def __str__(self):
            return f'the message from {self.sender} to {self.recipient}'

    class LoginHistory:
        """Класс таблицы истории входа пользователей в программу."""

        def __init__(self, user_id, ip_address, port, date_login):
            self.id = None
            self.user_id = user_id
            self.ip_address = ip_address
            self.port = port
            self.date_login = date_login

        def __str__(self):
            return f'the user {self.user_id} came in {self.date_login}'

    class UserContacts:
        """Класс таблицы контактов пользователей."""

        def __init__(self, user_id, contact):
            self.id = None
            self.user_id = user_id
            self.contact = contact

        def __str__(self):
            return f'the user {self.user_id} has contact with {self.contact}'

    class UserMessageHistory:
        """
        Класс таблицы статистики отправленных и полученных сообщений
        пользователей.
        """

        def __init__(self, user_id):
            self.id = None
            self.user_id = user_id
            self.sent_msg_num = 0
            self.accepted_msg_num = 0

        def __str__(self):
            return f'the user {self.user_id} sent {self.sent_msg_num} and' \
                   f' received {self.accepted_msg_num} messages'

    def __init__(self, db_name):
        self.engine = create_engine(
            f'sqlite:///{(db_name)}' +
            '?check_same_thread=False',
            echo=False,
            pool_recycle=7200)
        self.metadata = MetaData()

        users_table = Table('users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('date_register', DateTime),
                            Column('psw_hash', String),
                            Column('pubkey', Text)
                            )

        active_users_table = Table(
            'active_users', self.metadata, Column(
                'id', Integer, primary_key=True), Column(
                'user_id', ForeignKey('users.id'), unique=True), Column(
                'ip_address', String), Column(
                'port', Integer), Column(
                'date_login', DateTime))

        messages_table = Table('messages', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('sender', ForeignKey('users.id')),
                               Column('recipient', ForeignKey('users.id')),
                               Column('text_message', Text),
                               Column('send_date', DateTime),
                               )

        login_history_table = Table('login_history', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user_id', ForeignKey('users.id')),
                                    Column('ip_address', String),
                                    Column('port', Integer),
                                    Column('date_login', DateTime)
                                    )

        user_contacts_table = Table('user_contacts', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user_id', ForeignKey('users.id')),
                                    Column('contact', ForeignKey('users.id'))
                                    )

        user_msg_history_table = Table(
            'user_msg_history', self.metadata, Column(
                'id,', Integer, primary_key=True), Column(
                'user_id', ForeignKey('users.id')), Column(
                'sent_msg_num', Integer), Column(
                'accepted_msg_num', Integer))

        self.metadata.create_all(self.engine)

        mapper(self.Users, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.Messages, messages_table)
        mapper(self.LoginHistory, login_history_table)
        mapper(self.UserContacts, user_contacts_table)
        mapper(self.UserMessageHistory, user_msg_history_table)

        Session = sessionmaker(bind=self.engine)
        self.session_obj = Session()

        self.session_obj.query(self.ActiveUsers).delete()
        self.session_obj.commit()

    def create_user(self, name, psw_hash):
        """
        Создать запись в БД о новом пользователе.
        :param name: (str) Имя пользователя.
        :param psw_hash: (str) Захешированный пароль пользователя.
        """
        date = datetime.datetime.now()
        new_user = self.Users(name, date, psw_hash)
        self.session_obj.add(new_user)
        self.session_obj.commit()

        new_user_msg_history = self.UserMessageHistory(new_user.id)
        self.session_obj.add(new_user_msg_history)
        self.session_obj.commit()

    def del_user(self, user):
        """
        Удалить пользователя из БД сервера.
        :param user: (str) имя пользователя.
        """
        try:
            user_row = self.session_obj.query(
                self.Users).filter_by(
                name=user).first()
            self.session_obj.query(
                self.ActiveUsers).filter_by(
                user_id=user_row.id).delete()
            self.session_obj.query(
                self.Messages).filter(
                (self.Messages.sender == user_row.id) | (
                    self.Messages.recipient == user_row.id)).delete()
            self.session_obj.query(
                self.LoginHistory).filter_by(
                user_id=user_row.id).delete()
            self.session_obj.query(
                self.UserContacts).filter(
                (self.UserContacts.user_id == user_row.id) | (
                    self.UserContacts.contact == user_row.id)).delete()
            self.session_obj.query(
                self.UserMessageHistory).filter_by(
                user_id=user_row.id).delete()
            self.session_obj.query(self.Users).filter_by(name=user).delete()

            self.session_obj.commit()
        except exc.SQLAlchemyError:
            print('Ошибка обращения к БД при попытке удаления пользователя.')

    def log_in(self, name, ip_address, port, key):
        """
        Залогинить пользователя.
        :param name: (str) Имя пользователя.
        :param ip_address: (str) IP адрес пользователя.
        :param port: (int) Номер порта пользователя.
        :param key: (str) Публичный ключ пользователя.
        """
        try:
            records = self.session_obj.query(self.Users).filter_by(name=name)
            date = datetime.datetime.now()
            if not records.count():
                raise Exception('Пользователь не зарегистрирован.')
            else:
                user = records.first()
                if user.pubkey != key:
                    user.pubkey = key

            new_active_user = self.ActiveUsers(user.id, ip_address, port, date)
            self.session_obj.add(new_active_user)

            new_history = self.LoginHistory(user.id, ip_address, port, date)
            self.session_obj.add(new_history)

            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке залогинивания'
                ' пользователя.')

    def log_out(self, name):
        """
        Отработать выход пользователя.
        :param name: (str) Имя пользователя.
        """
        try:
            user = self.session_obj.query(
                self.Users).filter_by(
                name=name).first()
            if user:
                self.session_obj.query(
                    self.ActiveUsers).filter_by(
                    user_id=user.id).delete()
                self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_SERV.error('Ошибка обращения к БД при выходе пользователя.')

    def check_user(self, user):
        """
        Проверить существование пользователя.
        :param user: (str) Имя пользователя.
        :return: (bool) True - если пользователь существует, False - если нет.
        """
        try:
            records = self.session_obj.query(
                self.Users.name).filter_by(
                name=user).count()
            if records:
                return True
            else:
                return False
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при проверке на существование'
                ' пользователя.')

    def save_user_messages(self, sender, recipient, text_message):
        """
        Сохранить сообщение.
        :param sender: (str) Отправитель сообщения.
        :param recipient: (str) Получатель сообщения.
        :param text_message: (str) Текст сообщения.
        """
        try:
            user_sender = self.session_obj.query(
                self.Users).filter_by(
                name=sender).first()
            user_recipient = self.session_obj.query(
                self.Users).filter_by(
                name=recipient).first()
            date = datetime.datetime.now()
            new_message = self.Messages(
                user_sender.id, user_recipient.id, text_message, date)
            self.session_obj.add(new_message)
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке сохранения сообщения'
                ' пользователя.')

    def get_user_messages(self, sender=None, recipient=None):
        """
        Получить переданные сообщения.
        :param sender: (str, необязательный) Отправитель сообщения.
        По умолчанию None.
        :param recipient: (str, необязательный) Получатель сообщения.
        По умолчанию None.
        :return: Выборка сообщений.
        """
        try:
            if sender and not recipient:
                sender_obj = self.session_obj.query(
                    self.Users).filter_by(
                    name=sender).one()

                sub = self.session_obj.query(
                    self.Users.name.label('recipient')).join(
                    self.Messages,
                    self.Messages.recipient == self.Users.id).filter(
                    self.Messages.sender == sender_obj.id).subquery()

                records = self.session_obj.query(
                    self.Users.name,
                    sub.c.recipient,
                    self.Messages.text_message,
                    self.Messages.send_date).join(
                    self.Messages,
                    self.Messages.sender == self.Users.id).distinct().filter(
                    self.Users.id == sender_obj.id)

            elif not sender and recipient:
                recipient_obj = self.session_obj.query(
                    self.Users).filter_by(
                    name=recipient).one()

                sub = self.session_obj.query(
                    self.Users.name.label('sender')).join(
                    self.Messages,
                    self.Messages.sender == self.Users.id).filter(
                    self.Messages.recipient == recipient_obj.id).subquery()

                records = self.session_obj.query(
                    sub.c.sender,
                    self.Users.name,
                    self.Messages.text_message,
                    self.Messages.send_date).join(
                    self.Messages,
                    self.Messages.recipient == self.Users.id) \
                    .distinct().filter(self.Users.id == recipient_obj.id)
            else:
                sub = self.session_obj.query(self.Users.name
                                             .label('recipient')) \
                    .join(self.Messages, self.Messages.recipient
                          == self.Users.id) \
                    .subquery()

                records = self.session_obj.query(
                    self.Users.name,
                    sub.c.recipient,
                    self.Messages.text_message,
                    self.Messages.send_date).join(
                    self.Messages,
                    self.Messages.sender == self.Users.id).distinct()
            return records.all()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке получения сообщений'
                ' пользователей.')

    def get_hash(self, user):
        """
        Получить захешированный пароль пользователя.
        :param user: (str) Имя пользователя.
        :return: (bytes) Захешированный пароль пользователя.
        """
        try:
            hash = self.session_obj.query(
                self.Users.psw_hash).filter_by(
                name=user).first()[0]
            return hash
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке получения хеша пароля'
                ' пользователя.')

    def get_public_key(self, user):
        """
        Получить публичный ключ пользователя.
        :param user: (str) Имя пользователя.
        :return: (str) Публичный ключ пользователя.
        """
        try:
            public_key = self.session_obj.query(
                self.Users.pubkey).filter_by(
                name=user).one()[0]
            return public_key
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке получения публичного ключа'
                ' пользователя.')

    def get_all_users(self):
        """
        Получить всех пользователей.
        :return: Выборка всех пользователей.
        """
        try:
            records = self.session_obj.query(
                self.Users.name, self.Users.date_register)
            return [user for user, date in records]
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке получения всех'
                ' пользователей.')

    def get_active_users(self):
        """
        Получить активных пользователей.
        :return: Выборка активных пользователей.
        """
        try:
            records = self.session_obj.query(
                self.Users.name,
                self.ActiveUsers.ip_address,
                self.ActiveUsers.port,
                self.ActiveUsers.date_login).join(
                self.Users)
            return records.all()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке получения активных'
                ' пользователей.')

    def get_login_users_history(self, name=None):
        """
        Получить историю входа пользователей.
        :param name: (str, необязательный) Имя пользователя. По умолчанию None.
        :return: Выборка историй входа пользователей.
        """
        try:
            records = self.session_obj.query(
                self.Users.name,
                self.LoginHistory.ip_address,
                self.LoginHistory.port,
                self.LoginHistory.date_login).join(
                self.LoginHistory,
                self.Users.id == self.LoginHistory.user_id)
            if name:
                records = records.filter(self.Users.name == name)
            return records.all()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке получения истории входа'
                ' пользователей.')

    def add_message(self, sender, recipient):
        """
        Обновить статистику переданных и полученных сообщений пользователя.
        :param sender: (str) Отправитель сообщения.
        :param recipient: (str) Получатель сообщения.
        :return:
        """
        try:
            sender_obj = self.session_obj.query(
                self.Users).filter_by(
                name=sender).one()
            receiver_obj = self.session_obj.query(
                self.Users).filter_by(
                name=recipient).one()

            sender = self.session_obj.query(
                self.UserMessageHistory).filter_by(
                user_id=sender_obj.id).first()
            sender.sent_msg_num += 1

            receiver = self.session_obj.query(
                self.UserMessageHistory).filter_by(
                user_id=receiver_obj.id).first()
            receiver.accepted_msg_num += 1

            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке обновления статистики'
                ' сообщений.')

    def add_contact(self, user, contact):
        """
        Добавить новый контакт пользователю.
        :param user: (str) Имя пользователя.
        :param contact: (str) Добавляемый контакт.
        """
        try:
            user_obj = self.session_obj.query(
                self.Users).filter_by(
                name=user).one()
            contact_obj = self.session_obj.query(
                self.Users).filter_by(
                name=contact).first()

            if not contact_obj or self.session_obj.query(
                self.UserContacts).filter_by(
                    user_id=user_obj.id,
                    contact=contact_obj.id).count():
                return

            new_contact = self.UserContacts(user_obj.id, contact_obj.id)

            self.session_obj.add(new_contact)
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке добавления контакта.')

    def delete_contact(self, user, contact):
        """
        Удалить контакт пользователя.
        :param user: (str) Имя пользователя.
        :param contact: (str) Удаляемый контакт.
        """
        try:
            user_obj = self.session_obj.query(
                self.Users).filter_by(
                name=user).one()
            contact_obj = self.session_obj.query(
                self.Users).filter_by(
                name=contact).first()

            if not contact_obj:
                return

            self.session_obj.query(
                self.UserContacts).filter_by(
                user_id=user_obj.id,
                contact=contact_obj.id).delete()

            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_SERV.error(
                'Ошибка обращения к БД при попытке удаления контакта.')

    def get_contacts(self, user):
        """
        Получить контакты пользователя.
        :param user: (str) Имя пользователя.
        :return: Выборка контактов пользователя.
        """
        try:
            user_obj = self.session_obj.query(
                self.Users).filter_by(
                name=user).one()

            sub = self.session_obj.query(
                self.Users.name.label('contact')).join(
                self.UserContacts,
                self.UserContacts.contact == self.Users.id).filter(
                self.UserContacts.user_id == user_obj.id).subquery()

            records = self.session_obj.query(
                self.Users.name,
                sub.c.contact).join(
                self.UserContacts,
                self.UserContacts.user_id == self.Users.id).filter(
                self.Users.id == user_obj.id).distinct()
            return [contact for user, contact in records]
        except Exception:
            LOG_SERV.error('Ошибка обращения к БД при получении '
                           'контактов пользователя.')

    def get_statistics_msg(self):
        """
        Получить статистику по переданным и полученным
        сообщениям всех пользователей.
        :return: Выборка статистики полученных и
        переданных сообщений пользователей.
        """
        try:
            records = self.session_obj.query(self.Users.name,
                                             self.UserMessageHistory.
                                             sent_msg_num,
                                             self.UserMessageHistory.
                                             accepted_msg_num) \
                .join(self.UserMessageHistory, self.UserMessageHistory.user_id
                      == self.Users.id).distinct() \
                .order_by(self.Users.name)
            return records.all()
        except exc.SQLAlchemyError:
            LOG_SERV.error('Ошибка обращения к БД при получении статистики'
                           ' сообщений.')


if __name__ == '__main__':
    test = HandlerServDB(SERV_DB_NAME)

    # Создаём пользователей
    # test.create_user('test_user_1', '123')
    # test.create_user('test_user_2', '456')
    # test.create_user('test_user_3', '789')

    # Логиним пользователей
    test.log_in('test_user_1', '192.168.5.5', 9999, '456')
    test.log_in('test_user_2', '192.168.6.6', 12000, '123')

    # Выводим всех пользователей
    headers = ['имя', 'дата регистрации']
    print('Все пользователи')
    print(test.get_all_users())
    # print(tabulate(test.get_all_users(), headers=headers, tablefmt="pipe"))
    print('\n' * 2)

    # Отключаем одного из пользовалелей
    test.log_out('test_user_1')

    # Выводим активных пользовалелей
    print('Активные пользователи')
    print(tabulate(test.get_active_users(), headers=headers, tablefmt='pipe'))
    print('\n' * 2)

    # Логиним еще одного пользователя
    test.log_in('test_user_3', '192.168.7.7', 12312, '789')

    # Вновь выводим активных пользовалелей
    headers_active = ['имя', 'адрес', 'порт', 'время подключения']
    print('Активные пользователи после подключения еще одного')
    print(tabulate(test.get_active_users(), headers=headers_active,
                   tablefmt='pipe'))
    print('\n' * 2)

    # Отправляем сообщение пользователя и сохраняем его
    test.save_user_messages('test_user_1', 'test_user_3', 'Hello Third!')

    # Выводим историю логирования пользователей
    headers_login = ['имя', 'адрес', 'порт', 'дата']
    print('История логирования пользователей')
    print(tabulate(test.get_login_users_history(), headers=headers_login,
                   tablefmt='pipe'))
    print('\n' * 2)

    # Выводим историю логирования для одного пользователя
    print('История логирования одного пользователя')
    print(tabulate(test.get_login_users_history('test_user_1'),
                   headers=headers_login, tablefmt='pipe'))
    print('\n' * 2)

    # Выводим сообщения пользователей
    print('Сообщения пользователей')
    headers_messages = ['отправитель', 'получатель', 'текст', 'дата']
    print(tabulate(test.get_user_messages(sender='test_user_1'),
                   headers=headers_messages, tablefmt='pipe'))
    print('\n' * 2)

    # Получаем хеш пароля пользователя
    print('Захешированный пароль пользователя')
    print(test.get_hash('test_user_1'))
    print('\n' * 2)

    # Получаем публичный ключ пользователя
    print('Публичный ключ пользователя')
    print(test.get_public_key('test_user_1'))
    print('\n' * 2)

    # Посылаем сообщение
    test.add_message('test_user_1', 'test_user_2')

    # Добавляем контакты пользователям
    test.add_contact('test_user_1', 'test_user_2')
    test.add_contact('test_user_1', 'test_user_3')
    test.add_contact('test_user_2', 'test_user_3')

    test.add_contact('user', 'test_user_1')
    test.add_contact('user', 'test_user_2')
    test.add_contact('user', 'test_user_3')

    # Удаляем контакты пользователям
    test.delete_contact('test_user_2', 'test_user_3')

    # Получаем список контактов пользователя
    print('Список контактов пользователя')
    print(test.get_contacts('test_user_1'))
    print('\n' * 2)

    # Получаем статистику по переданным и полученным сообщениям
    headers_statistic = ['пользователь', 'кол-во отпр. сообщ.',
                         'кол-во перед. сообщ.']
    print('Статистика сообщений')
    print(tabulate(test.get_statistics_msg(), headers=headers_statistic,
                   tablefmt='pipe'))
    print('\n' * 2)
