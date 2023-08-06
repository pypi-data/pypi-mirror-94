"""Функции"""

import json
from logging import getLogger

from common.decos import log
from common.constants import ENCODING, SIZE_PACKET
from common.errors import NoBytesDataError, NoDictDataError,\
    InvalidPortNumberError


LOG = getLogger('log_client')


@log
# @Log()
def get_data(sock, size_pack=SIZE_PACKET):
    """
    Получение сообщения, преобразование его в байты => строка => словарь.
    :param sock: (socket) Сокет принимающей стороны.
    :param size_pack: (int, необязательный) Допустимый размер пакета
    передаваемых данных. По умолочанию 10240.
    :return: (dict) Словарь содержащий сообщение.
    """
    data = sock.recv(size_pack)
    if isinstance(data, bytes):
        decode_data = data.decode(ENCODING)
        dict_message = json.loads(decode_data)
        if isinstance(dict_message, dict):
            return dict_message
        else:
            raise NoDictDataError
    else:
        raise NoBytesDataError


def send_data(sock, message):
    """
    Отправка сообщения, преобразование его в словарь => строка => байты.
    :param sock: (socket) Сокет отправляющей стороны.
    :param message: (dict) Словарь с сообщением.
    """
    try:
        js_message = json.dumps(message)
        sock.send(js_message.encode(ENCODING))
    except ConnectionError:
        LOG.error('Попытка отправления сообщения потерпела неудачу')


@log
# @Log()
def validate_port_number(port_number):
    """
    Валидация введенного значения порта.
    :param port_number: (int) Номер порта.
    :return: (int) Номер порта после валидации.
    """
    if port_number < 1024 or port_number > 65535:
        raise InvalidPortNumberError(port_number)
    return port_number
