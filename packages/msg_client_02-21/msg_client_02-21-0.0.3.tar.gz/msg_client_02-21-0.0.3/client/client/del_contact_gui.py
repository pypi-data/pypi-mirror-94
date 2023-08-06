"""Окно удаления контакта."""
import sys

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton,\
    QApplication
from PyQt5.QtCore import Qt

from client.client_database import HandlerClientDB


class DelContactWindow(QDialog):
    """Класс окна удаления контакта пользователя."""

    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setFixedSize(300, 200)
        self.setWindowTitle('Удаление контакта')
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.label = QLabel(
            'Выберите пользователя для удаления из контактов', self)
        self.label.move(5, 5)

        self.selector = QComboBox(self)
        self.selector.setGeometry(5, 25, 170, 20)

        self.del_btn = QPushButton('Удалить', self)
        self.del_btn.setGeometry(180, 25, 100, 30)

        self.cancel_btn = QPushButton('Отмена', self)
        self.cancel_btn.setGeometry(180, 60, 100, 30)
        self.cancel_btn.clicked.connect(self.close)

        self.fill_contacts()

    def fill_contacts(self):
        """Заполнить имеющимися контактами пользователя раскрывающийся
         список."""
        contacts = self.database.get_contacts()
        self.selector.addItems(sorted(contacts))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_database = HandlerClientDB('test')
    test_database.add_contact('test_1')
    test_database.add_contact('test_2')
    del_contact_window = DelContactWindow(test_database)
    del_contact_window.show()
    app.exec_()
