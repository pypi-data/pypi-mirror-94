"""Декораторы"""

from logging import getLogger

import traceback

from common.errors import NoAuthorizeError


LOG = getLogger('log_client')


def log(func):
    """Функция-декоратор, записывающий в лог-файл информацию о вызываемой
    функции, её параметрах, а также откуда эта функция была вызвана."""

    def wrapper(*args, **kwargs):
        """Функция-обёртка"""
        LOG.debug(
            f'Функция {func.__name__} была вызвана из функции'
            f' {traceback.format_stack()[0].strip().split()[-1]}'
            f' c параметрами {args}, {kwargs}', stacklevel=2)
        result = func(*args, **kwargs)
        return result

    return wrapper


class Log:
    """Класс-декоратор, записывающий в лог-файл информацию о вызываемой
     функции, её параметрах, а также откуда эта функция была вызвана."""

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            """Функция-обёртка"""
            LOG.debug(
                f'Функция {func.__name__} была вызвана из функции'
                f' {traceback.format_stack()[0].strip().split()[-1]}'
                f' c параметрами {args}, {kwargs}', stacklevel=2)
            result = func(*args, **kwargs)
            return result

        return wrapper


class LoginRequired:
    """Класс-декоратор, проверяющий авторизован ли пользователь."""

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            """Функция-обёртка"""
            from socket import socket
            from server.server.core import HandlerMessage
            from common.constants import ACTION, TIME, TYPE_ACTION_PUBLIC_KEY
            if args[1][ACTION] == TYPE_ACTION_PUBLIC_KEY:
                if isinstance(
                    args[0],
                    HandlerMessage) and isinstance(
                    args[1],
                    dict) and ACTION in args[1] and TIME in args[1] and\
                        isinstance(args[2],
                        socket) and args[2] in args[0].names_to_sock.values():
                    LOG.warning('Проверка авторизации пользователя: успех.')
                    return func(*args, **kwargs)
                else:
                    raise NoAuthorizeError
            else:
                return func(*args, **kwargs)

        return wrapper
