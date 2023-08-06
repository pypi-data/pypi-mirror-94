"""Дескрипторы"""

from logging import getLogger

from common.errors import InvalidPortNumberError


LOG = getLogger('log_client')


class ValidHost:
    """Класс дескриптора, проверяющий адрес."""

    def __set_name__(self, owner, host):
        self.host = host

    def __set__(self, instance, value):
        if not isinstance(value, str):
            LOG.critical(f'Неверный формат данных: {type(value)}!')
            raise TypeError('Значение должно иметь формат строки!')
        instance.__dict__[self.host] = value


class ValidPort:
    """Класс дескриптора, проверяющий порт."""

    def __set_name__(self, owner, port):
        self.port = port

    def __set__(self, instance, value):
        if not isinstance(value, int):
            LOG.critical(f'Неверный формат данных: {type(value)}!')
            raise TypeError('Значение должно быть целочисленным!')
        if value < 1024 or value > 65535:
            LOG.critical(
                f'Указан некорректный номер порта: {value},'
                f' соединение закрывается')
            raise InvalidPortNumberError(value)
        instance.__dict__[self.port] = value
