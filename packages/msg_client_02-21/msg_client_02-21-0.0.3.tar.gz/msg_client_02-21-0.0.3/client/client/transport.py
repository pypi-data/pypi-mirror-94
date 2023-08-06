"""Скрипт содержащий логику работы клиентской части."""
import sys
import json
import time
import hmac
import hashlib
import binascii
from logging import getLogger
from threading import Thread, Lock

from socket import socket, AF_INET, SOCK_STREAM, error
from PyQt5.QtCore import QObject, pyqtSignal

from common.functions import get_data, send_data
from common.constants import TYPE_ACTION_PRESENCE, ACTION, TIME, TYPE,\
    STATUS, USER, ACCOUNT_NAME, PUBLIC_KEY, TYPE_ACTION_MESSAGE, FROM, TO,\
    TYPE_ACTION_LEAVE, TYPE_ACTION_GET_CONTACTS, TYPE_ACTION_GET_USERS, \
    TYPE_ACTION_DELETE_CONTACT, CONTACT, TYPE_ACTION_ADD_CONTACT, \
    TYPE_ACTION_PUBLIC_KEY, RESPONSE, SUCCESS_CODE_RESPONSE, \
    ACCEPTED_CODE_RESPONSE, CREATED_CODE_RESPONSE, ALERT, \
    AUTH_REQUIRED_RESPONSE, RESET_CONTENT_RESPONSE, ERROR_CODE_RESPONSE, \
    ERROR, DATA, MESSAGE, WRONG_PASSWORD
from common.errors import MissingFieldError, WrongTypeActionError

LOG_CLIENT = getLogger('log_client')
sock_lock = Lock()


class ClientTransport(Thread, QObject):
    """Класс клиента - приёмник и передатчик сообщений с сервером."""
    new_message = pyqtSignal(dict)
    connection_lost = pyqtSignal()
    message_205 = pyqtSignal()

    def __init__(
            self,
            serv_host,
            serv_port,
            database,
            user_name,
            password,
            keys):
        Thread.__init__(self)
        QObject.__init__(self)
        self.user_name = user_name
        self.database = database
        self.password = password
        self.keys = keys
        self.client_sock = None
        self.put_through(serv_host, serv_port)
        try:
            self.update_users_list()
            self.update_contact_list()
        except OSError as e:
            if e.errno:
                LOG_CLIENT.critical('Соединение с сервером было потеряно1.')
            LOG_CLIENT.error(
                'Время для соединения с сервером при обновлении списка'
                ' пользователей вышло.')
            sys.exit(1)
        except json.JSONDecodeError:
            LOG_CLIENT.critical('Соединение с сервером было потеряно2.')
            sys.exit(1)
        self.running = True

    def put_through(self, host, port):
        """
        Соединить с сервером подключенного клиента.
        :param host: (str) IP адрес сервера;
        :param port: (int) Порт по которому сервер принимает сообщения
        клиентов;
        """
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.settimeout(5)

        LOG_CLIENT.info('Подключение клиента к серверу')
        connect_flag = False
        for i in range(5):
            try:
                LOG_CLIENT.info(f'Попытка №{i + 1}')
                self.client_sock.connect((host, port))
            except (OSError, ConnectionRefusedError, error):
                pass
            else:
                connect_flag = True
                LOG_CLIENT.info('Соединение с сервером установлено!')
                break
            time.sleep(1)

        if not connect_flag:
            LOG_CLIENT.critical(
                f'Подключение не установлено, т.к. конечный компьютер отверг'
                f' запрос на подключение')
            sys.exit(1)

        try:
            msg_presence = self.create_message(TYPE_ACTION_PRESENCE)
            with sock_lock:
                send_data(self.client_sock, msg_presence)
            LOG_CLIENT.debug(
                f'Сообщение клиента о присутствии отправлено на сервер')
            self.check_answer()
        except (OSError, ConnectionRefusedError):
            LOG_CLIENT.critical('Соединение с сервером было потеряно3.')
            sys.exit(1)

    def create_message(self, type_message, contact=None, text_message=None):
        """
        Создать сообщение клиента в соответствиии с протоколом JIM.
        :param type_message: (str) Тип передаваемого сообщения.
        :param contact: (str, необязательный) Имя контакта пользователя.
        :param text_message: (str, необязательный) Текст сообщения.
        :return: (dict) Словарь с сообщением пользователя в соответствии
        протоколу JIM.
        """
        if type_message is TYPE_ACTION_PRESENCE:
            LOG_CLIENT.debug('Создано сообщения клиента серверу о присутствии')
            pubkey = self.keys.publickey().export_key().decode('ascii')
            return {
                ACTION: TYPE_ACTION_PRESENCE,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                TYPE: STATUS,
                USER: {
                    ACCOUNT_NAME: self.user_name,
                    PUBLIC_KEY: pubkey
                },
            }

        elif type_message is TYPE_ACTION_MESSAGE:
            LOG_CLIENT.debug('Создано сообщениe клиента')
            return {
                ACTION: TYPE_ACTION_MESSAGE,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                FROM: self.user_name,
                TO: contact,
                MESSAGE: text_message,
            }

        elif type_message is TYPE_ACTION_LEAVE:
            return {
                ACTION: TYPE_ACTION_LEAVE,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                USER: self.user_name,
            }

        elif type_message is TYPE_ACTION_GET_CONTACTS:
            return {
                ACTION: TYPE_ACTION_GET_CONTACTS,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                USER: self.user_name,
            }

        elif type_message is TYPE_ACTION_GET_USERS:
            return {
                ACTION: TYPE_ACTION_GET_USERS,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                USER: self.user_name,
            }

        elif type_message is TYPE_ACTION_DELETE_CONTACT:
            return {
                ACTION: TYPE_ACTION_DELETE_CONTACT,
                USER: self.user_name,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                CONTACT: contact
            }
        elif type_message is TYPE_ACTION_ADD_CONTACT:
            return {
                ACTION: TYPE_ACTION_ADD_CONTACT,
                USER: self.user_name,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S'),
                CONTACT: contact
            }
        elif type_message is TYPE_ACTION_PUBLIC_KEY:
            return {
                ACTION: TYPE_ACTION_PUBLIC_KEY,
                USER: self.user_name,
                CONTACT: contact,
                TIME: time.strftime('%d.%m.%Y %H:%M:%S')
            }

    def check_answer(self):
        """Получить и проверить сообщение от сервера."""
        try:
            with sock_lock:
                data = get_data(self.client_sock)
            LOG_CLIENT.debug(f'Проверка ответа от сервера: {data}')
            if RESPONSE in data:
                if RESPONSE in data:
                    if data[RESPONSE] == SUCCESS_CODE_RESPONSE:
                        LOG_CLIENT.info(
                            'Сообщение о присутствии подтверждено.')
                        return True

                    elif data[RESPONSE] == ACCEPTED_CODE_RESPONSE:
                        LOG_CLIENT.debug('Сообщение об успехе')
                        return True

                    elif data[RESPONSE] == CREATED_CODE_RESPONSE:
                        LOG_CLIENT.debug('Сообщение об успехе')
                        return data[ALERT]

                    elif data[RESPONSE] == AUTH_REQUIRED_RESPONSE:
                        return self.authorize_on_serv(data)

                    elif data[RESPONSE] == RESET_CONTENT_RESPONSE:
                        self.message_205.emit()
                        self.update_users_list()
                        self.update_contact_list()
                        LOG_CLIENT.info(
                            'Сгенерирован сигнал об обновлении списка'
                            ' контактов.')

                    elif data[RESPONSE] == ERROR_CODE_RESPONSE:
                        LOG_CLIENT.warning(
                            f'Сообщение об ошибке: {data[ERROR]}')
                        if data[ERROR] == WRONG_PASSWORD:
                            self.client_sock.close()
                            sys.exit(0)
                        return False

                else:
                    raise MissingFieldError(RESPONSE)
            elif ACTION in data:
                if TIME in data and FROM in data and TO in data and MESSAGE\
                        in data and data[ACTION] == TYPE_ACTION_MESSAGE:
                    LOG_CLIENT.debug(
                        f'Получено сообщение от пользователя {data[FROM]}')
                    self.new_message.emit(data)
                    return data[MESSAGE]

                elif ACTION not in data:
                    raise MissingFieldError(ACTION)
                elif TIME not in data:
                    raise MissingFieldError(TIME)
                elif FROM not in data:
                    raise MissingFieldError(FROM)
                elif MESSAGE not in data:
                    raise MissingFieldError(MESSAGE)
                elif data[ACTION] != TYPE_ACTION_MESSAGE:
                    raise WrongTypeActionError(
                        TYPE_ACTION_MESSAGE, data[ACTION])

        except OSError as e:
            if e.errno:
                LOG_CLIENT.critical('Потеряно соединение с сервером.')
                self.running = False
                self.connection_lost.emit()
        except (ConnectionError, ConnectionAbortedError, ConnectionResetError,
                json.JSONDecodeError):
            LOG_CLIENT.critical('Потеряно соединение с сервером.')
            self.running = False
            self.connection_lost.emit()
        except TypeError:
            self.message_205.emit()

    def authorize_on_serv(self, data):
        """
        Захешировать пароль пользователя, вычислить результат HMAC-функции от
        полученного от сервера сообщения используя захешированный пароль в
        качестве ключа, и отправить сообщение серверу для авторизации.
        :param data: (dict) Полученный от сервера словарь-сообщение с
        запросом на авторизацию.
        :return: (bool) True - успех авторизации, False - ошибка авторизации.
        """
        passw_bytes = self.password.encode('utf-8')
        salt_bytes = self.user_name.upper().encode('utf-8')
        passw_hash = hashlib.pbkdf2_hmac(
            'sha256', passw_bytes, salt_bytes, 100000)
        passw_hash_str = binascii.hexlify(passw_hash)
        serv_answer = data[DATA]
        hash = hmac.new(passw_hash_str, serv_answer.encode('utf-8'), 'sha256')
        digest = hash.digest()
        digest = binascii.b2a_base64(digest).decode('ascii')
        msg_authorize = {RESPONSE: AUTH_REQUIRED_RESPONSE, DATA: digest}
        try:
            send_data(self.client_sock, msg_authorize)
            if self.check_answer():
                return True
        except (OSError, json.JSONDecodeError):
            LOG_CLIENT.error('Сбой соединения в процессе авторизации')
            return False

    def update_users_list(self):
        """Запросить на сервере список пользователей и обновить в клиентской
        базе данных таблицу пользователей."""
        LOG_CLIENT.info(
            f'Запрос списка известных пользователей для {self.user_name}')
        msg_get_users = self.create_message(TYPE_ACTION_GET_USERS)
        with sock_lock:
            send_data(self.client_sock, msg_get_users)
        result = self.check_answer()
        if result:
            result.remove(self.user_name)
        LOG_CLIENT.info(
            f'Получен ответ от сервера о известных пользователях'
            f' {self.user_name}: {result}')
        LOG_CLIENT.info(
            'Запущен процесс внесения пользователей в базу данных...')
        self.database.add_users(result)
        LOG_CLIENT.info(
            'Список известных пользователей успешно внесен в базу данных!')
        check = self.database.get_users()
        LOG_CLIENT.info(f'Проверка: {check == result}')

    def update_contact_list(self):
        """Запросить на сервере список контактов пользователя и обновить в
        клиентской базе данных таблицу контактов."""
        LOG_CLIENT.info(
            f'Запрос контакт листа для пользователя {self.user_name}')
        self.database.delete_all_contacts()
        msg_get_contacts = self.create_message(TYPE_ACTION_GET_CONTACTS)
        with sock_lock:
            send_data(self.client_sock, msg_get_contacts)
        result = self.check_answer()
        LOG_CLIENT.info(
            f'Получен ответ от сервера о контактах {self.user_name}: {result}')

        LOG_CLIENT.info('Запущен процесс внесения контактов в базу данных...')
        for contact in result:
            self.database.add_contact(contact)
        LOG_CLIENT.info('Список контактов успешно внесен в базу данных!')
        check = self.database.get_contacts()
        LOG_CLIENT.info(f'Проверка: {check == result}')

    def add_contact(self, contact):
        """
        Добавить новый контакт пользователю.
        :param contact: (str) Имя добавляемого в контакт пользователя.
        """
        LOG_CLIENT.info(f'Создание контакта {contact}')
        msg_add_contact = self.create_message(
            TYPE_ACTION_ADD_CONTACT, contact=contact)
        with sock_lock:
            send_data(self.client_sock, msg_add_contact)
        result = self.check_answer()
        if not result:
            LOG_CLIENT.error(
                f'Попытка добавить в контакты пользователя {contact} потерпела'
                f' неудачу')

    def delete_contact(self, contact):
        """
        Удалить из списка контактов пользователя требуемый контакт.
        :param contact: (str) Имя удаляемого из контактов пользователя.
        """
        LOG_CLIENT.info(f'Удаление контакта {contact}')
        msg_del_contact = self.create_message(
            TYPE_ACTION_DELETE_CONTACT, contact=contact)
        with sock_lock:
            send_data(self.client_sock, msg_del_contact)
        result = self.check_answer()
        if not result:
            LOG_CLIENT.error(
                f'Попытка удалить из контактов пользователя {contact}'
                f' потерпела неудачу')

    def key_request(self, user):
        """
        Запросить для требуемого пользователя с кем открывается беседа его
        публичный ключ.
        :param user: (str) Имя пользователя - собеседника.
        :return: (str) Публичный ключ пользователя - собеседника.
        """
        LOG_CLIENT.info(f'Запрос публичного ключа для {user}')
        msg_key_request = self.create_message(
            TYPE_ACTION_PUBLIC_KEY, contact=user)
        with sock_lock:
            send_data(self.client_sock, msg_key_request)
        public_key = self.check_answer()
        if not public_key:
            LOG_CLIENT.error(
                f'Запрос на получение публичного ключа пользователя {user}'
                f' потерпела неудачу.')
        return public_key

    def exit_user(self):
        """Отправить словарь с типом сообщения о выходе из программы."""
        self.running = False
        msg_leave = self.create_message(TYPE_ACTION_LEAVE)
        try:
            with sock_lock:
                send_data(self.client_sock, msg_leave)
        except OSError:
            pass
        LOG_CLIENT.info('Транспорт завершает работу')
        time.sleep(0.5)

    def send_message(self, recipient, text_message):
        """
        Сформировать словарь с сообщением и отправить пользователю.
        :param recipient: (str) Имя получаетеля.
        :param text_message: (str) Текст сообщения.
        """
        LOG_CLIENT.info(f'Отправление сообщения пользователю {recipient}')
        msg = self.create_message(
            TYPE_ACTION_MESSAGE,
            contact=recipient,
            text_message=text_message)
        with sock_lock:
            send_data(self.client_sock, msg)
        result = self.check_answer()
        if not result:
            LOG_CLIENT.error('Попытка отправить сообщение потерпела неудачу')

    def run(self):
        """Запустить поток приёма сообщений с сервера."""
        LOG_CLIENT.debug('Запущен процесс - приемник сообщений с сервера.')
        while self.running:
            time.sleep(3)
            self.client_sock.settimeout(0.5)
            self.check_answer()
            self.client_sock.settimeout(5)
