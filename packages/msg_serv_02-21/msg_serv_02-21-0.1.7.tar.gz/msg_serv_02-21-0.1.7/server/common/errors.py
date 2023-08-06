"""Собственные исключения."""

import argparse


class MissingFieldError(Exception):
    """Исключение - требумое поле отсутствует в сообщении."""

    def __init__(self, lost_field):
        super().__init__(lost_field)
        self.lost_field = lost_field

    def __str__(self):
        return f'В сообщении отсутствует поле {self.lost_field}.'


class WrongTypeActionError(Exception):
    """Исключение - сообщение содержит неверные данные."""
    def __init__(self, expected_value, current_value):
        super().__init__(expected_value, current_value)
        self.expected_value = expected_value
        self.current_value = current_value

    def __str__(self):
        return f'Сообщение содержит поле {self.current_value} вместо' \
               f' ожидаемого {self.expected_value}.'


class AnswerServerError(Exception):
    """Исключение - ощибка ответа сервера."""
    def __init__(self, comment):
        super().__init__(comment)
        self.comment = comment

    def __str__(self):
        return f'Ответ сервера содержит ошибку: {self.comment}.'


class NoBytesDataError(Exception):
    """Исключение - данные получены не в байтовом формате."""

    def __str__(self):
        return 'Данные не в байтовом формате.'


class NoDictDataError(Exception):
    """Исключение - тип данных не словарь."""

    def __str__(self):
        return 'Тип данных не является словарём.'


class InvalidPortNumberError(Exception):
    """Исключение - указан некорректный номер порта."""

    def __init__(self, invalid_port):
        super().__init__(invalid_port)
        self.invalid_port = invalid_port

    def __str__(self):
        return f'Номер порта {self.invalid_port} является недопустимым! ' \
               f'Допустимые значения от 1024 до 65535.'


class WrongModeClientError(Exception):
    """Исключение - не указан или неверно указан режим клиента."""

    def __str__(self):
        return 'Режим для клиента не указан или указан неверно! Допустимые' \
               ' режимы: send(отправка), listen(получение) сообщения.'


class MissingArgumentParser(argparse.ArgumentParser):
    """Переопределение вывода сообщения об ошибках в библиотеке argparse."""

    def __init__(self):
        super().__init__()

    def error(self, message):
        raise WrongModeClientError


class NoAuthorizeError(Exception):
    """Исключение - пользователь не зарегистрирован."""

    def __str__(self):
        return 'Пользователь не зарегистрирован!'
