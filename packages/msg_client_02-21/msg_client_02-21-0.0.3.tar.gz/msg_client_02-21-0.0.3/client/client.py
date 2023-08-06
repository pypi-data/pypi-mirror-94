"""Скрипт запуска клиента."""

import sys
import os
from threading import Lock
from logging import getLogger

from PyQt5.QtWidgets import QApplication
from Cryptodome.PublicKey import RSA

from common.errors import MissingArgumentParser
from common.constants import DEFAULT_HOSTNAME, DEFAULT_PORT
from client.main_window import ClientMainWindow
from client.client_database import HandlerClientDB
from client.welcome_gui import WelcomeWindow
from client.transport import ClientTransport
from log.log_config import client_log_config

LOG_CLIENT = getLogger('log_client')

sock_lock = Lock()
database_lock = Lock()


def get_param():
    """
    Проверка введенных параметров подключения и установка соединения с
    сервером.
    Значения параметров по умолчанию:
    адрес хоста: 127.0.0.1
    порт: 8888
    :return:
    """
    parser = MissingArgumentParser()
    parser.add_argument(
        'addr',
        default=DEFAULT_HOSTNAME,
        help='Адрес сервера',
        nargs='?')
    parser.add_argument(
        'port',
        default=DEFAULT_PORT,
        help='Номер порта для подключения к серверу',
        type=int,
        nargs='?')
    parser.add_argument(
        '-n',
        '--name',
        default=None,
        help='Имя пользователя',
        nargs='?')
    parser.add_argument(
        '-p',
        '--password',
        default=None,
        help='Пароль пользователя',
        nargs='?')

    args = parser.parse_args()

    serv_host = args.addr
    serv_port = args.port
    user_name = args.name
    user_password = args.password

    return serv_host, serv_port, user_name, user_password


def main():
    """Запустить в работу клиентскую часть."""
    sys.path.append('./client')
    serv_host, serv_port, user_name, password = get_param()
    client_app = QApplication(sys.argv)

    if not user_name:
        welcome_window = WelcomeWindow()
        client_app.exec_()
        if welcome_window.flag:
            user_name = welcome_window.input_name.text()
            if not password:
                password = welcome_window.input_password.text()
            del welcome_window
        else:
            sys.exit(0)

    LOG_CLIENT.info(
        f'Запущен клиент с параметрами: адрес сервера: {serv_host}, порт:'
        f' {serv_port}, имя пользователя {user_name}')

    database = HandlerClientDB(user_name)
    transport = None
    key_file = os.path.join(os.getcwd(), f'{user_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048)
        with open(key_file, 'wb') as f:
            f.write(keys.export_key())
    else:
        with open(key_file, 'rb') as f:
            keys = RSA.import_key(f.read())
    LOG_CLIENT.info('Ключи успешно загружены.')
    try:
        transport = ClientTransport(
            serv_host,
            serv_port,
            database,
            user_name,
            password,
            keys)
    except Exception as e:
        print(e)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()

    main_window = ClientMainWindow(database, transport, keys)
    main_window.create_connection(transport)
    main_window.setWindowTitle(f'Messenger v.0.0.1 - {user_name}')
    client_app.exec_()

    transport.exit_user()
    transport.join()


if __name__ == '__main__':
    main()

