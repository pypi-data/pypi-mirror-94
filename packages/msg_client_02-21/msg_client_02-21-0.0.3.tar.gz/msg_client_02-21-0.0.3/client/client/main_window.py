"""Главное окно клиентской части."""
import sys
import json
import base64
from logging import getLogger

from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSlot
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA

from client.main_window_conv import Ui_MainClientWindow
from client.add_contact_gui import AddContactWindow
from client.del_contact_gui import DelContactWindow
from client.client_database import HandlerClientDB
from common.constants import MESSAGE, FROM, TO
from log.log_config import client_log_config

LOG_CLIENT = getLogger('log_client')


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно клиента. Назначает обработчики событий, заполняет
    контентом виджеты главного окна клиента.
    """

    def __init__(self, database, transport, keys):
        super().__init__()
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)
        self.database = database
        self.transport = transport

        self.decrypter = PKCS1_OAEP.new(keys)

        self.ui.action_exit.triggered.connect(qApp.exit)

        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.action_add_contact.triggered.connect(self.add_contact_window)

        self.ui.btn_del_contact.clicked.connect(self.del_contact_window)
        self.ui.action_del_contact.triggered.connect(self.del_contact_window)

        self.ui.btn_send_message.clicked.connect(self.send_msg)

        self.contacts_model = None
        self.history_model = QStandardItemModel()
        self.messages = QMessageBox()
        self.current_contact = None
        self.current_contact_key = None
        self.encryptor = None

        self.ui.contacts_list.doubleClicked.connect(
            self.choice_current_contact)

        self.update_clients_list()
        self.turn_off_widgets()
        self.show()

    def turn_off_widgets(self):
        """Очистить поле ввода сообщений, а также сделать его и кнопки
         управления сообщением неактивными."""
        self.ui.lbl_input_new_msg.setText(
            'Выберите получателя дважды кликнув по нему:')
        self.ui.text_msg.clear()
        self.history_model.clear()

        self.ui.btn_clear_field.setDisabled(True)
        self.ui.btn_send_message.setDisabled(True)
        self.ui.text_msg.setDisabled(True)

        self.current_contact = None
        self.current_contact_key = None
        self.encryptor = None

    def update_messages_list(self):
        """Обновить виджет с сообщениями."""
        data_messages = self.database.get_messages()
        data_messages = sorted(data_messages, key=lambda item: item[3])
        self.ui.messages_list.setModel(self.history_model)

        self.history_model.clear()

        count_msg = len(data_messages)
        if count_msg > 20:
            first_index = count_msg - 20
        else:
            first_index = 0

        for i in range(first_index, count_msg):
            item = data_messages[i]
            if item[0] == self.current_contact:
                msg_field = QStandardItem(
                    f'Исходящее сообщение от {item[3].replace(microsecond=0)}:'
                    f'\n{item[2]}')
                msg_field.setEditable(False)
                msg_field.setBackground((QBrush(QColor(230, 220, 61))))
                msg_field.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(msg_field)
            elif item[1] == self.current_contact:
                msg_field = QStandardItem(
                    f'Входящее сообщение от {item[3].replace(microsecond=0)}:'
                    f'\n{item[2]}')
                msg_field.setEditable(False)
                msg_field.setBackground((QBrush(QColor(130, 221, 212))))
                msg_field.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(msg_field)
            self.ui.messages_list.scrollToBottom()

    @pyqtSlot()
    def choice_current_contact(self):
        """Получить из контакт листа текущий контакт."""
        self.current_contact = self.ui.contacts_list.currentIndex().data()
        self.set_current_contact()

    def set_current_contact(self):
        """Установить в качестве контакта выбранного пользователя."""
        try:
            self.current_contact_key = self.transport.key_request(
                self.current_contact)
            LOG_CLIENT.info(f'Загружен открытый ключ для {self.current_contact}')
            if self.current_contact_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_contact_key))
        except (OSError, json.JSONDecodeError):
            self.current_contact_key = None
            self.encryptor = None
            LOG_CLIENT.warning(
                f'Не удалось получить ключ для {self.current_contact}')

            if not self.current_contact_key:
                self.messages.warning(
                    self, 'Ошибка', 'Для выбранного пользователя нет ключа'
                                    ' шифрования.')
                return

        self.ui.lbl_input_new_msg.setText(
            f'Сообщение для {self.current_contact}:')
        self.ui.btn_clear_field.setDisabled(False)
        self.ui.btn_send_message.setDisabled(False)
        self.ui.text_msg.setDisabled(False)

        self.update_messages_list()

    def update_clients_list(self):
        """Обновить список пользователей."""
        contacts = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.contacts_list.setModel(self.contacts_model)

    def add_contact_window(self):
        """Создать объект окна для добавления контакта."""
        global choice_dialog
        choice_dialog = AddContactWindow(self.database, self.transport)
        choice_dialog.add_btn.clicked.connect(
            lambda: self.add_contact_action(choice_dialog))
        choice_dialog.show()

    def add_contact_action(self, item):
        """
        Считать выбранного пользователя и закрыть окно добавления контакта.
        :param item: (QDialog) Объект окна добавления контакта.
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """
        Добавить выбранного пользователя в контакты.
        :param new_contact: (str) Новый контакт пользователя.
        """
        try:
            self.transport.add_contact(new_contact)
        except OSError as e:
            if e.errno:
                self.messages.critical(
                    self, 'Ошибка', 'Потеряно соединение с сервером')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения')
        else:
            self.database.add_contact(new_contact)
            LOG_CLIENT.info(f'Создан новый контакт {new_contact}')
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)

            self.messages.information(
                self, 'Успех', 'Контакт успешно добавлен')

    def del_contact_window(self):
        """Создать объект окна для удаления контакта."""
        global del_dialog
        del_dialog = DelContactWindow(self.database)
        del_dialog.del_btn.clicked.connect(
            lambda: self.del_contact(del_dialog))
        del_dialog.show()

    def del_contact(self, item):
        """
        Удалить выбранного пользователя из контактов.
        :param item: (QDialog) Объект окна для удаления контакта.
        """
        contact = item.selector.currentText()
        try:
            self.transport.delete_contact(contact)
        except OSError as e:
            if e.errno:
                self.messages.critical(
                    self, 'Ошибка', 'Потеряно соединение с сервером')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения')
        else:
            self.database.delete_contact(contact)
            self.update_clients_list()
            LOG_CLIENT.info(f'Контакт {contact} был удалён')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён')
            item.close()
            if contact == self.current_contact:
                self.current_contact = None
                self.turn_off_widgets()

    def send_msg(self):
        """Зашифровать, закодировать и отправить сообщение на сервер."""
        text_message = self.ui.text_msg.toPlainText()
        self.ui.text_msg.clear()
        if not text_message:
            return

        text_message_encrypted = self.encryptor.encrypt(
            text_message.encode('utf-8'))
        text_msg_enc_base64 = base64.b64encode(text_message_encrypted)

        try:
            self.transport.send_message(
                self.current_contact,
                text_msg_enc_base64.decode('ascii'))
        except OSError as e:
            if e.errno:
                self.messages.critical(
                    self, 'Ошибка', 'Потеряно соединение с сервером.')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения')
            LOG_CLIENT.critical(e)
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(
                self, 'Ошибка', 'Потеряно соединение с сервером.')
            self.close()
        else:
            self.database.save_message(
                self.current_contact,
                self.transport.user_name,
                text_message)
            LOG_CLIENT.info(
                f'Сообщение пользователю {self.current_contact} отправлено')
            self.update_messages_list()

    @pyqtSlot(dict)
    def recv_message(self, data):
        """
        Раскодировать, расшифровывать и сохранить сообщение в БД клиента.
        :param data: (dict) Словарь сообщения клиента в соответствии с
        протоколом JIM.
        """
        text_message_encrypted = base64.b64decode(data[MESSAGE])
        try:
            text_message_decrypted = self.decrypter.decrypt(
                text_message_encrypted)
        except (ValueError, TypeError):
            LOG_CLIENT.warning('Не удалось декодировать сообщение.')
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return
        self.database.save_message(data[TO],
                                   data[FROM],
                                   text_message_decrypted.decode('utf-8'))

        sender = data[FROM]
        if sender == self.current_contact:
            self.update_messages_list()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(
                    self,
                    'Новое сообщение',
                    f'Получено новое сообщение от '
                    f'{sender}, открыть чат с ним?',
                    QMessageBox.Yes,
                        QMessageBox.No) == QMessageBox.Yes:
                    self.current_contact = sender
                    self.set_current_contact()
            else:
                if self.messages.question(
                    self,
                    'Новое сообщение',
                    f'Получено новое сообщение от '
                    f'{sender}.\nЭтот пользователь отсутствует в ваших'
                    f' контактах. Добавить?',
                    QMessageBox.Yes,
                        QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_contact = sender
                    self.set_current_contact()

    @pyqtSlot()
    def connection_lost(self):
        """Вывести сообщение об ошибке соединения и закрыть главное окно."""
        self.messages.warning(
            self,
            'Ошибка соединения',
            'Потеряно соединение с сервером.')
        self.close()

    @pyqtSlot()
    def sig_205(self):
        """
        Проверить существует ли ещё пользователь с кем происходит общение.
        """
        if self.current_contact and not self.database.check_contact(
                self.current_contact):
            self.messages.warning(
                self,
                'Внимание',
                f'Пользователь {self.current_contact} был удалён!')
            self.turn_off_widgets()
            self.current_contact = None
        self.update_clients_list()

    def create_connection(self, trans_obj):
        """
        Назначить обработчики событий.
        :param trans_obj: (ClientTransport) Объект класса клиента приёмника
        и передатчика сообщений.
        """
        trans_obj.new_message.connect(self.recv_message)
        trans_obj.connection_lost.connect(self.connection_lost)
        trans_obj.message_205.connect(self.sig_205)


class Test:
    """Класс-заглушка для тестирования работоспособности главного окна
     пользователя."""

    def __init__(self, user_name):
        self.user_name = user_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_database = HandlerClientDB('test')

    test_transport = Test('test')

    test_keys = '123'

    my_window = ClientMainWindow(test_database, test_transport, test_keys)
    app.exec_()
