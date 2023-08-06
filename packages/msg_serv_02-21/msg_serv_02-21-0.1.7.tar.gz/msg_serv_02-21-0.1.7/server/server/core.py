"""Скрипт ядра серверной части."""

import os
import select
import hmac
import binascii
from logging import getLogger
from threading import Thread

from socket import socket, AF_INET, SOCK_STREAM
from PyQt5.QtCore import pyqtSignal

from common.constants import MAX_CONNECTIONS, USER, ACCOUNT_NAME, RESPONSE, \
    ERROR_CODE_RESPONSE, ERROR, DUPLICATE_NAME_ERROR_COMMENT, \
    AUTH_REQUIRED_RESPONSE, DATA, USER_NOT_EXISTS_COMMENT, \
    SUCCESS_CODE_RESPONSE, PUBLIC_KEY, WRONG_PASSWORD, ACTION, TIME, \
    TYPE_ACTION_PRESENCE, FROM, TO, MESSAGE, TYPE_ACTION_MESSAGE, CONTACT, \
    TYPE_ACTION_DELETE_CONTACT, ACCEPTED_CODE_RESPONSE, \
    TYPE_ACTION_ADD_CONTACT, TYPE_ACTION_GET_CONTACTS, CREATED_CODE_RESPONSE, \
    ALERT, TYPE_ACTION_GET_USERS, TYPE_ACTION_PUBLIC_KEY, TYPE_ACTION_LEAVE, \
    ERROR_COMMENT, RESET_CONTENT_RESPONSE
from common.functions import get_data, send_data
from common.decos import log, LoginRequired
from common.descriptors import ValidHost, ValidPort

LOG_SERV = getLogger('log_serv')


class HandlerMessage(Thread):
    """Класс сервера - обработчик принимаемых сообщений и отправления ответа
    клиентам."""
    serv_host = ValidHost()
    """Дескриптор атрибута IP адреса сервера."""

    serv_port = ValidPort()
    """Дескриптор атрибута номера порта сервера."""



    def __init__(self, serv_host, serv_port, database):
        super().__init__()
        self.serv_host = serv_host
        self.serv_port = serv_port
        self.database = database
        self.clients = []
        self.messages_list = []
        self.names_to_sock = {}
        self.running = True
        self.serv_sock = None

    def run(self):
        """Запустить поток сервера для приёма, обработки, передачи сообщений.

        Создать сокет сервера, привязать параметры подключения, установить
        в режим прослушивания,
        получить сообщения от клиента, вывод сообщения в консоль, отправить
        ответ клиенту.
        """
        LOG_SERV.debug('Создание сокета сервера')
        serv_sock = socket(AF_INET, SOCK_STREAM)
        self.serv_sock = serv_sock
        self.serv_sock.bind((self.serv_host, self.serv_port))
        LOG_SERV.debug(
            f'Привязка сокета к IP адресу: {self.serv_host} и порту машины:'
            f' {self.serv_port}')
        self.serv_sock.settimeout(1)
        self.serv_sock.listen(MAX_CONNECTIONS)
        LOG_SERV.debug(
            f'Сокет сервера готов принимать соединения, максимальное число'
            f' соедиений в очереди:'
            f' {MAX_CONNECTIONS}')
        while True:
            try:
                client_sock, addr = self.serv_sock.accept()
            except OSError:
                pass
            else:
                LOG_SERV.info(
                    f'Клиент {client_sock.fileno()}'
                    f' {client_sock.getpeername()} подключился к серверу')
                self.clients.append(client_sock)
            finally:
                wait = 0
                recv_list = None
                send_list = None
                try:
                    recv_list, send_list, errors_list = select.select(
                        self.clients, self.clients, [], wait)
                    LOG_SERV.debug(
                        f'Количество клиентов передающих данные: '
                        f'{len(recv_list)}')
                    LOG_SERV.debug(
                        f'Количество клиентов принимающих данные:'
                        f' {len(send_list)}')
                except select.error:
                    pass
                if recv_list:
                    self.get_message(recv_list)
                if self.messages_list and send_list:
                    self.send_message()

    @log
    def get_message(self, recv_list):
        """
        Перебрать список клиентов, отправивших сообщение, получить их
        сообщения и сгенерировать ответ клиентам.
        :param recv_list: (list) Список клиентов отправивших сообщение на
        сервер.
        """
        for sock in recv_list:
            message_dict = get_data(sock)
            LOG_SERV.debug(
                f'Получены данные от клиента: {sock.fileno()}'
                f' {sock.getpeername()}')
            resp_to_client = self.create_response_message(message_dict, sock)
            LOG_SERV.debug(
                f'Создан ответ на запрос от клиента : {sock.fileno()}'
                f' {sock.getpeername()}')
            if not resp_to_client:
                self.turn_sock_off(sock)

    def authorize_user(self, sock, data):
        """
        Авторизовать пользователя: вычислить HMAC-функцию для сгенерированного
        набора случайных байт, используя в качестве ключа захешированный
        пароль пользователя, отправить случайный набор байт клиенту, получить
        от него ответ и сравнить полученные значения: в случае совпадения
        авторизовать пользователя.
        :param sock: (socket) Сокет клиента, для которого проводится
        авторизация.
        :param data: (dict) Словарь-сообщение с запросом авторизации,
        полученный от пользователя.
        """
        LOG_SERV.info(
            f'Запуск процесса аутентификации пользователя'
            f' {data[USER][ACCOUNT_NAME]}')
        if data[USER][ACCOUNT_NAME] in self.names_to_sock.keys():
            response_msg = {
                RESPONSE: ERROR_CODE_RESPONSE,
                ERROR: DUPLICATE_NAME_ERROR_COMMENT}
            try:
                LOG_SERV.info(
                    f'Такое имя уже занято, отправление ответа {response_msg}')
                send_data(sock, response_msg)
            except OSError:
                LOG_SERV.warning('Ошибка отправления ответа о занятом имени.')
            self.turn_sock_off(sock)

        elif not self.database.check_user(data[USER][ACCOUNT_NAME]):
            response_msg = {
                RESPONSE: ERROR_CODE_RESPONSE,
                ERROR: USER_NOT_EXISTS_COMMENT}
            try:
                LOG_SERV.info(
                    f'Пользователя с таким именем не существует, отправление'
                    f' ответа {response_msg}')
                send_data(sock, response_msg)
            except OSError:
                LOG_SERV.warning(
                    'Ошибка отправления ответа о несуществующем пользователе.')
                self.turn_sock_off(sock)

        else:
            LOG_SERV.info('Имя пользователя корректно')
            random_str = binascii.hexlify(os.urandom(32))
            auth_msg = {
                RESPONSE: AUTH_REQUIRED_RESPONSE,
                DATA: random_str.decode('ascii')}
            hash = hmac.new(
                self.database.get_hash(
                    data[USER][ACCOUNT_NAME]),
                random_str,
                'sha256')
            digest = hash.digest()
            try:
                send_data(sock, auth_msg)
                answer = get_data(sock)
            except OSError:
                LOG_SERV.warning(
                    'Ошибка при передаче запроса о аутентификации.')
                self.turn_sock_off(sock)
                return
            client_digest = binascii.a2b_base64(answer[DATA])
            if RESPONSE in answer and hmac.compare_digest(
                    digest, client_digest):
                self.names_to_sock[data[USER][ACCOUNT_NAME]] = sock
                response_msg = {RESPONSE: SUCCESS_CODE_RESPONSE}
                try:
                    send_data(sock, response_msg)
                except OSError:
                    LOG_SERV.warning(
                        'Ошибка при передаче ответа об успешной'
                        ' аутентификации.')
                    self.turn_sock_off(sock)
                self.database.log_in(
                    data[USER][ACCOUNT_NAME],
                    *sock.getpeername(),
                    data[USER][PUBLIC_KEY])
            else:
                response_msg = {
                    RESPONSE: ERROR_CODE_RESPONSE,
                    ERROR: WRONG_PASSWORD}
                try:
                    send_data(sock, response_msg)
                except OSError:
                    LOG_SERV.warning(
                        'Ошибка при передаче ответа с ошибкой о неверном'
                        ' пароле.')
                    self.turn_sock_off(sock)

    @log
    @LoginRequired()
    def create_response_message(self, data, sock):
        """
        Сформировать ответ сервера клиенту в зависимости от корректности
        сообщения от клиента.
        :param data: (dict) Словарь-сообщение, полученный от пользователя.
        :param sock: (socket) Сокет пользователя.
        :return: (bool) True - если полученное сообщение о продолжении работы
        в программе,
        False - если сообщение с запросом о выходе из программы.
        """
        LOG_SERV.debug(f'Проверка сообщения от клиента: {data}')
        if ACTION in data and TIME in data and USER in data and ACCOUNT_NAME \
                in data[USER] and PUBLIC_KEY in data[USER] and data[ACTION] \
                == TYPE_ACTION_PRESENCE:
            self.authorize_user(sock, data)
            self.names_to_sock[data[USER][ACCOUNT_NAME]] = sock
            LOG_SERV.debug('Сообщение корректно, ответ: ОК')
            return True

        elif ACTION in data and TIME in data and FROM in data and TO in data \
                and MESSAGE in data and data[ACTION] == TYPE_ACTION_MESSAGE:
            if data[TO] in self.names_to_sock:
                response_msg = {RESPONSE: SUCCESS_CODE_RESPONSE}

                data_list_response = [data[FROM], response_msg]
                self.messages_list.append(data_list_response)

                data_list = [data[TO], data]

                self.database.add_message(data[FROM], data[TO])
                self.database.save_user_messages(
                    data[FROM], data[TO], data[MESSAGE])
                self.messages_list.append(data_list)

            else:
                response_msg = {
                    RESPONSE: ERROR_CODE_RESPONSE,
                    ERROR: USER_NOT_EXISTS_COMMENT}
                data_list = [data[FROM], response_msg]
                LOG_SERV.error(USER_NOT_EXISTS_COMMENT)
                self.messages_list.append(data_list)
            return True

        elif ACTION in data and USER in data and TIME in data and CONTACT in \
                data and data[ACTION] == TYPE_ACTION_DELETE_CONTACT and \
                data[USER] in self.names_to_sock:
            self.database.delete_contact(data[USER], data[CONTACT])
            response_msg = {RESPONSE: ACCEPTED_CODE_RESPONSE}
            data_list = [data[USER], response_msg]
            self.messages_list.append(data_list)
            return True

        elif ACTION in data and USER in data and TIME in data and CONTACT in \
                data and data[ACTION] == TYPE_ACTION_ADD_CONTACT and \
                data[USER] in self.names_to_sock:
            self.database.add_contact(data[USER], data[CONTACT])
            response_msg = {RESPONSE: ACCEPTED_CODE_RESPONSE}
            data_list = [data[USER], response_msg]
            self.messages_list.append(data_list)
            return True

        elif ACTION in data and TIME in data and USER in data and \
                data[ACTION] == TYPE_ACTION_GET_CONTACTS \
                and data[USER] in self.names_to_sock:
            contacts = self.database.get_contacts(data[USER])
            response_msg = {RESPONSE: CREATED_CODE_RESPONSE, ALERT: contacts}
            data_list = [data[USER], response_msg]
            self.messages_list.append(data_list)
            return True

        elif ACTION in data and TIME in data and USER in data and\
                data[ACTION] == TYPE_ACTION_GET_USERS \
                and data[USER] in self.names_to_sock:
            users = self.database.get_all_users()
            response_msg = {RESPONSE: CREATED_CODE_RESPONSE, ALERT: users}
            data_list = [data[USER], response_msg]
            self.messages_list.append(data_list)
            return True

        elif ACTION in data and TIME in data and USER in data and \
                data[ACTION] == TYPE_ACTION_PUBLIC_KEY \
                and CONTACT in data and data[USER] in self.names_to_sock:
            public_key = self.database.get_public_key(data[CONTACT])
            response_msg = {RESPONSE: CREATED_CODE_RESPONSE, ALERT: public_key}
            data_list = [data[USER], response_msg]
            self.messages_list.append(data_list)
            return True

        elif ACTION in data and TIME in data and USER in data and \
                data[ACTION] == TYPE_ACTION_LEAVE and data[USER] \
                in self.names_to_sock:
            return False
        else:
            LOG_SERV.error(
                'Сообщение не прошло проверку, ответ: неверный запрос')
            return {RESPONSE: ERROR_CODE_RESPONSE, ERROR: ERROR_COMMENT}

    def turn_sock_off(self, sock):
        """Записать в лог-файл сообщение об ошибке,
        удалить сокет из списка сокетов и закрыть соединение.
        :param sock: (socket) Сокет пользователя.
        """
        LOG_SERV.info(
            f'Клиент {sock.fileno()} {sock.getpeername()} отключился от'
            f' сервера')

        name = [name for name, value in self.names_to_sock.items()
                if value == sock][0]

        self.database.log_out(name)
        self.names_to_sock.pop(name)
        self.clients.remove(sock)
        sock.close()

    def send_message(self):
        """
        Перебрать список клиентов, ожидающих принять сообщение и отправить им
        ответ сервера.
        """

        for msg in self.messages_list:
            recipient = msg[0]
            recipient_sock = self.names_to_sock[recipient]
            try:
                send_data(recipient_sock, msg[1])
                LOG_SERV.debug(
                    f'Клиенту {recipient_sock.fileno()}'
                    f' {recipient_sock.getpeername()} отправлен ответ:'
                    f' {msg[1]}')
            except ConnectionError:
                self.turn_sock_off(recipient_sock)
            self.messages_list.remove(msg)

    def service_update_lists(self, user):
        """
        Отправить всем подключенным сейчас пользователям сообщение с запросом
        на обновление контактов и известных пользователей.
        :param user: (str) Имя пользователя зарегистрированного или удалённого
        из программы.
        """
        for client in self.clients:
            response_msg = {RESPONSE: RESET_CONTENT_RESPONSE, ALERT: user}
            send_data(client, response_msg)
