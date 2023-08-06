"""БД клиента."""
import os
import datetime
from logging import getLogger

from tabulate import tabulate
from sqlalchemy import create_engine, MetaData, Table, Column, Integer,\
    String, Text, DateTime, exc
from sqlalchemy.orm import mapper, sessionmaker
from log.log_config import client_log_config
from sqlalchemy.sql import default_comparator

LOG_CLIENT = getLogger('log_client')

if os.path.split(os.getcwd())[1] == 'client':
    PATH_DIR = ''
else:
    PATH_DIR = './client'


class HandlerClientDB:
    """
        Класс - оболочка для работы с базой данных клиента.
        Использует SQLite базу данных, реализован с помощью
        SQLAlchemy ORM и используется классический подход.
        """

    class KnownUsers:
        """Класс таблицы известных пользователю других пользователей."""

        def __init__(self, user):
            self.id = None
            self.user = user

        def __str__(self):
            return f'Known user: {self.user}'

    class Contacts:
        """Класс таблицы контактов пользователя."""

        def __init__(self, contact):
            self.id = None
            self.contact = contact

        def __str__(self):
            return f'The contact {self.contact}'

    class MessageHistory:
        """Класс таблицы истории сообщений пользователя."""

        def __init__(self, sender, recipient, text_message, send_date):
            self.id = None
            self.sender = sender
            self.recipient = recipient
            self.text_message = text_message
            self.send_date = send_date

        def __str__(self):
            return f'The message to {self.recipient}'

    def __init__(self, name):
        self.engine = create_engine(
            # f'sqlite:///{PATH_DIR}/{name}_database' +
            f'sqlite:///{name}_database' +
            '?check_same_thread=False',
            echo=False,
            pool_recycle=7200)
        self.metadata = MetaData()

        known_users = Table('known_users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('user', String)
                            )

        contacts_table = Table('contacts', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('contact', String, unique=True)
                               )

        message_table = Table('messages', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('sender', String),
                              Column('recipient', String),
                              Column('text_message', Text),
                              Column('send_date', DateTime)
                              )

        self.metadata.create_all(self.engine)

        mapper(self.KnownUsers, known_users)
        mapper(self.Contacts, contacts_table)
        mapper(self.MessageHistory, message_table)

        Session = sessionmaker(bind=self.engine)
        self.session_obj = Session()

        self.session_obj.query(self.Contacts).delete()
        self.session_obj.commit()

    def add_users(self, users_list):
        """
        Добавить известных пользователю других пользователей.
        :param users_list: (list) Список известных пользователей полученный
        с БД сервера.
        """
        try:
            self.session_obj.query(self.KnownUsers).delete()
            for user in users_list:
                _user = self.KnownUsers(user)
                self.session_obj.add(_user)
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке добавления известного'
                ' пользователя.')

    def add_contact(self, contact):
        """
        Добавить контакт пользователю.
        :param contact: (str) Имя пользователя добавляемого в контакты.
        """
        try:
            new_contact = self.Contacts(contact)
            self.session_obj.add(new_contact)
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке добавления контакта.')

    def delete_all_contacts(self):
        """Удалить все контакты пользователя."""
        try:
            self.session_obj.query(self.Contacts).delete()
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_CLIENT.error('Попытка удалить контакты потерпела неудачу.')

    def delete_contact(self, contact):
        """
        Удалить из контактов указанного пользователя.
        :param contact: (str) Имя пользователя удаляемого из контактов.
        """
        try:
            self.session_obj.query(
                self.Contacts).filter_by(
                contact=contact).delete()
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке удаления контакта.')

    def get_contacts(self):
        """
        Возвратить все контакты пользователя.
        :return: Выборка всех контактов пользователя.
        """
        try:
            records = self.session_obj.query(self.Contacts.contact)
            return [contact[0] for contact in records]
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке получения контактов.')

    def check_contact(self, contact):
        """
        Проверить есть ли указанный пользователь в контактах.
        :param contact: (str) Имя пользователя.
        :return: (bool) True - пользователь есть в контактах, False -
        отсутствует.
        """
        try:
            if self.session_obj.query(
                    self.Contacts).filter_by(
                    contact=contact).count():
                return True
            else:
                return False
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при проверке на существование'
                ' контакта.')

    def get_users(self):
        """
        Возвратить всех известных пользователю других пользователей.
        :return: Выборка всех известных пользователей.
        """
        try:
            records = self.session_obj.query(self.KnownUsers.user)
            return [user[0] for user in records]
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке получения известных'
                ' пользователей.')

    def check_user(self, user):
        """
        Проверить есть ли указанный пользователь в таблице известных
        пользователей.
        :param user: (str) Имя пользователя.
        :return: (bool) True - Пользователь существет, False -
        отсутствует.
        """
        try:
            if self.session_obj.query(
                    self.KnownUsers).filter_by(
                    user=user).count():
                return True
            else:
                return False
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при проверке на существование'
                ' пользователя.')

    def save_message(self, sender, recipient, text):
        """
        Сохранить сообщение пользователя.
        :param sender: (str) Отправитель сообщения.
        :param recipient: (str) Получатель сообщения.
        :param text: (str) Текст сообщения.
        """
        try:
            date = datetime.datetime.now()
            new_message = self.MessageHistory(sender, recipient, text, date)
            self.session_obj.add(new_message)
            self.session_obj.commit()
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке сохранения сообщения.')

    def get_messages(self, sender=None, recipient=None):
        """
        Возвратить историю сообщений пользователя.
        :param sender: (str, необязательный) Отправитель сообщения.
        :param recipient: (str, необязательный) Получатель сообщения.
        :return: Выборка всех сообщений пользователя.
        """
        try:
            if sender:
                records = self.session_obj.query(
                    self.MessageHistory.sender,
                    self.MessageHistory.recipient,
                    self.MessageHistory.text_message,
                    self.MessageHistory.send_date).filter_by(
                    sender=sender)
            elif recipient:
                records = self.session_obj.query(
                    self.MessageHistory.sender,
                    self.MessageHistory.recipient,
                    self.MessageHistory.text_message,
                    self.MessageHistory.send_date).filter_by(
                    recipient=recipient)
            else:
                records = self.session_obj.query(
                    self.MessageHistory.sender,
                    self.MessageHistory.recipient,
                    self.MessageHistory.text_message,
                    self.MessageHistory.send_date)
            return records.all()
        except exc.SQLAlchemyError:
            LOG_CLIENT.error(
                'Ошибка обращения к БД при попытке получения сообщений.')


if __name__ == '__main__':
    print(os.path.abspath(os.getcwd()))

    test = HandlerClientDB('test_user_1')

    # Добавляем контакты пользователю
    test.add_contact('test_user_2')
    test.add_contact('test_user_3')
    test.add_contact('test_user_4')

    # Добавляем известных пользователей
    test.add_users(['test_user_10', 'test_user_11', 'test_user_12'])

    # Получаем контакты пользователя
    # print(tabulate(test.get_contacts(), headers=['контакты'],
    # tablefmt='pipe'))
    print('Контакты пользователя')
    print(test.get_contacts())
    print('\n' * 2)

    # Удаляем контакт пользователя
    test.delete_contact('test_user_4')

    # Убеждаемся в удалении контакта
    print('Контакты пользователя после удаления')
    print(test.get_contacts())
    # print(tabulate(test.get_contacts(), headers=['контакты'],
    # tablefmt='pipe'))
    print('\n' * 2)

    # Проверяем на наличие контакта
    print('Проверка на наличие контакта')
    print('test_user_2:', test.check_contact('test_user_2'))
    print('test_user_100:', test.check_contact('test_user_100'))
    print('\n' * 2)

    # Получаем известных пользователей
    print('Известные пользователи')
    print(test.get_users())
    print('\n' * 2)

    # Проверка на наличие известного пользователя
    print('Проверка на наличие известного пользователя')
    print('test_user_10:', test.check_user('test_user_10'))
    print('test_user_1:', test.check_user('test_user_1'))
    print('\n' * 2)

    # Сохраняем сообщения пользователя
    # test.save_message('test_user_1', 'test_user_2', 'hello test_user_2!')
    # test.save_message('test_user_1', 'test_user_3', 'hi test_user_3!')
    # test.save_message('test_user_1', 'test_user_1', 'hi himself!')

    # Получаем отправленные сообщения пользователя
    print('Отправленные сообщения')
    print(
        tabulate(
            test.get_messages(
                sender='test_user_1'),
            headers=[
                'получатель',
                'текст',
                'дата отправления'],
            tablefmt='pipe'))
    print('\n' * 2)

    # Получаем полученные сообщения пользователя
    print('Полученные сообщения')
    print(
        tabulate(
            test.get_messages(
                recipient='test_user_1'),
            headers=[
                'отправитель',
                'текст',
                'дата отправления'],
            tablefmt='pipe'))
    # print(test.get_messages(recipient='test_user_1'))
