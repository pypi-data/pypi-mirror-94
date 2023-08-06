"""Собственные метаклассы"""

import dis
from socket import socket


class ClientVerifier(type):
    """
    Метакласс, контролирующий используемые классом "Клиент" атрибуты и методы.
    """

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args)
        for name in kwargs:
            setattr(obj, name, kwargs[name])

        global_var = set()
        methods = set()

        method_names = ['accept', 'listen']
        attr_names = ['AF_INET', 'SOCK_STREAM']

        for item in cls.__dict__:
            if isinstance(cls.__dict__[item], socket):
                raise Exception('Ошибка! Сокет был создан на уровне класса!')
            try:
                instructions = dis.get_instructions(cls.__dict__[item])
            except TypeError:
                pass
            else:
                for i in instructions:
                    if i.opname == 'LOAD_GLOBAL':
                        global_var.add(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        methods.add(i.argval)

        for i in method_names:
            if i in methods:
                raise Exception(
                    f'Ошибка! Метод {i} не может быть использован для'
                    f' клиентского приложения')

        for i in attr_names:
            if i not in global_var:
                raise Exception(
                    f'Ошибка! Отсутствуют необходимый для создания сокета'
                    f' параметр: {i}')
        return obj


class ServerVerifier(type):
    """
    Метакласс, контролирующий используемые классом "Сервер" атрибуты и методы.
    """

    def __new__(mcs, name, bases, dct):

        global_var = set()
        methods = set()

        method_name = 'connect'
        attr_names = ['AF_INET', 'SOCK_STREAM']

        for item in dct:
            try:
                instructions = dis.get_instructions(dct[item])
            except TypeError:
                pass
            else:
                for i in instructions:
                    if i.opname == 'LOAD_GLOBAL':
                        global_var.add(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        methods.add(i.argval)

        for i in attr_names:
            if i not in global_var:
                raise Exception(
                    f'Ошибка! Отсутствуют необходимый для создания сокета'
                    f' параметр: {i}')
        if method_name in methods:
            raise Exception(
                f'Ошибка! Метод {method_name} не может быть использован для'
                f' серверного приложения')
        return type.__new__(mcs, name, bases, dct)
