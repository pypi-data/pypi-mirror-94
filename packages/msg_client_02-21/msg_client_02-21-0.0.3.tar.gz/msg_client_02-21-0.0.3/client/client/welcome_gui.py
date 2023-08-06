"""Окно приветствия."""
import sys

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton,\
    QApplication, qApp


class WelcomeWindow(QDialog):
    """Класс окна приветствия для ввода логина и пароля пользователя."""

    def __init__(self):
        super().__init__()

        self.flag = False

        self.setFixedSize(250, 200)
        self.setWindowTitle('Приветствуем Вас!')

        self.label_name = QLabel('Введите ваше имя:', self)
        self.label_name.move(10, 5)

        self.input_name = QLineEdit(self)
        self.input_name.setGeometry(10, 25, 200, 25)

        self.label_password = QLabel('Введите пароль:', self)
        self.label_password.move(10, 65)

        self.input_password = QLineEdit(self)
        self.input_password.setGeometry(10, 85, 200, 25)

        self.start_btn = QPushButton('Начать', self)
        self.start_btn.setGeometry(20, 130, 80, 30)
        self.start_btn.clicked.connect(self.start)

        self.exit_btn = QPushButton('Выход', self)
        self.exit_btn.setGeometry(120, 130, 80, 30)
        self.exit_btn.clicked.connect(qApp.exit)

        self.show()

    def start(self):
        """
        Проверить введены ли данные пользователем и если да, то запусить
        скрипт клиентской части.
        """
        if self.input_name.text() and self.input_password.text():
            self.flag = True
            qApp.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    app.exec_()
