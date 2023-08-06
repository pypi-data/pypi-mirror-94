"""Окно добавления контакта."""
import sys
from logging import getLogger

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton,\
    QApplication
from PyQt5.QtCore import Qt

from client.client_database import HandlerClientDB
from log.log_config import client_log_config

logger = getLogger('log_client')


class AddContactWindow(QDialog):
    """Класс окна добавления контакта пользователя."""

    def __init__(self, database, transport):
        super().__init__()
        self.database = database
        self.transport = transport

        self.setFixedSize(300, 200)
        self.setWindowTitle('Добавление контакта')
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.label = QLabel(
            'Выберите пользователя для добавления в контакты', self)
        self.label.move(5, 5)

        self.selector = QComboBox(self)
        self.selector.setGeometry(5, 25, 170, 20)

        self.update_btn = QPushButton('Обновить список', self)
        self.update_btn.setGeometry(40, 70, 100, 30)
        self.update_btn.clicked.connect(self.update_available_contacts)

        self.add_btn = QPushButton('Добавить', self)
        self.add_btn.setGeometry(180, 25, 100, 30)

        self.cancel_btn = QPushButton('Отмена', self)
        self.cancel_btn.setGeometry(180, 60, 100, 30)
        self.cancel_btn.clicked.connect(self.close)

        self.set_available_contacts()

    def set_available_contacts(self):
        """Выбрать доступные контакты."""
        self.selector.clear()

        contacts = self.database.get_contacts()
        contacts_list = set(contacts)

        users = self.database.get_users()
        users_list = set(users)

        self.selector.addItems(sorted(list(users_list - contacts_list)))

    def update_available_contacts(self):
        """Обновить доступные контакты."""
        try:
            self.transport.update_users_list()
        except OSError:
            pass
        else:
            logger.info('Обновление списка пользователей с сервера выполнено.')
            self.set_available_contacts()


class Test:
    """Класс-заглушка для тестирования работоспособности окна добавления
     контакта."""
    def __init__(self, user_name):
        self.user_name = user_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_database = HandlerClientDB('test')
    test_database.add_contact('test_1')
    test_database.add_users(['test', 'test_1', 'test_2', 'test_3'])
    test_transport = Test('test')

    add_contact_window = AddContactWindow(test_database, test_transport)
    add_contact_window.show()
    app.exec_()
