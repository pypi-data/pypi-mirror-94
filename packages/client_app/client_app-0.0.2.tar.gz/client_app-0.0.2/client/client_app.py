import argparse
import binascii
import hashlib
import hmac
import json
import logging
import os
import socket
import sys
import threading
import time

from Cryptodome.PublicKey import RSA
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication

import log.configs.client_log_config
from client.client_database import ClientDatabase
from client.main_window_client import MainWindowClient
from client.start_dialog import UserNameDialog
from common.errors import ServerError
from common.settings import RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PRESENCE, ACTION, TIME, ACCOUNT_NAME, \
    MESSAGE_TEXT, MESSAGE, SENDER, EXIT, CONTACT_LIST, USER, ADD_CONTACT, USERS_REQUEST, DELETE_CONTACT, DATA, \
    PASSWORD, PUBLIC_KEY, RESPONSE_511, DATA_LIST, PUBLIC_KEY_REQUEST
from common.utils import send_message, receiving_message

client_logger = logging.getLogger('client')

sock_lock = threading.Lock()
database_lock = threading.Lock()


class Client(threading.Thread, QObject):
    # class Client(metaclass=ClientVerifier):
    # class Client(threading.Thread, metaclass=ClientVerifier):
    new_message = pyqtSignal(dict)
    connection_lost = pyqtSignal()

    def __init__(
            self,
            server_addr,
            server_port,
            client_name,
            database,
            client_passwd,
            keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.socket = None
        self.client_name = client_name
        self.database = database
        self.client_passwd = client_passwd
        self.keys = keys
        # super().__init__()

        self.init_socket(server_addr, server_port)
        self.autorization()

        try:
            self.user_list_request()
            self.contact_list_request()
        except OSError as err:
            if err.errno:
                client_logger.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            client_logger.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            client_logger.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    def init_socket(self, server_addr, server_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.settimeout(5)

        # self.socket.connect((server_addr, server_port))

        connected = False
        for i in range(5):
            client_logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.socket.connect((server_addr, server_port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                client_logger.debug(
                    f"Соединение с сервером установлено c {i + 1} попытки.")
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            client_logger.critical(
                'Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

    def autorization(self):
        # pubkey = self.keys.publickey().export_key().decode('ascii')

        with sock_lock:
            presense = self.generating_presence_message(self.client_name)
            client_logger.debug(
                f"Presense сообщение на сервер = {presense[0]}")
            # Отправляем серверу приветственное сообщение.
            try:
                send_message(self.socket, presense[0])
                response = receiving_message(self.socket)
                client_logger.debug(f'Ответ сервера = {response}.')
                # print(response)
                if RESPONSE in response:
                    if response[RESPONSE] == 400:
                        raise ServerError(response[ERROR])
                    elif response[RESPONSE] == 511:
                        response_data = response[DATA]
                        hash = hmac.new(
                            presense[1], response_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.socket, my_ans)
                        self.pars_response_from_server(
                            receiving_message(self.socket))
            except (OSError, json.JSONDecodeError) as err:
                client_logger.debug(f'Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

    def run(self):
        # receiver = threading.Thread(target=self.message_from_server, args=(self.socket, self.client_name))
        # receiver = threading.Thread(target=self.message_from_server)
        # receiver.daemon = True
        # receiver.start()
        # return receiver

        while self.running:
            time.sleep(1)
            message = None
            with sock_lock:
                try:
                    self.socket.settimeout(0.5)
                    message = receiving_message(self.socket)
                except OSError as err:
                    if err.errno:
                        client_logger.critical(
                            f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    client_logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.socket.settimeout(5)

            if message:
                client_logger.debug(f'Принято сообщение с сервера: {message}')
                self.pars_response_from_server(message)

    # def run_sender(self):
    #     # interface = threading.Thread(target=self.user_interface, args=(self.socket, self.client_name))
    #     interface = threading.Thread(target=self.user_interface)
    #     interface.daemon = True
    #     interface.start()
    #     return interface

    def key_request(self, user):
        client_logger.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with sock_lock:
            send_message(self.socket, req)
            ans = receiving_message(self.socket)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            client_logger.error(f'Не удалось получить ключ собеседника{user}.')

    # @Log()
    def generating_presence_message(self, account_name='guest'):

        byte_client_passwd = self.client_passwd.encode('utf-8')
        byte_client_name = self.client_name.encode('utf-8')
        hash_client_passwd = hashlib.pbkdf2_hmac(
            'sha256', byte_client_passwd, byte_client_name, 100000)
        hash_client_passwd_str = binascii.hexlify(hash_client_passwd)

        pubkey = self.keys.publickey().export_key().decode('ascii')

        presense_dict = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name,
                PUBLIC_KEY: pubkey,
                PASSWORD: hash_client_passwd_str.decode('ascii')
            }
        }
        client_logger.info(
            f'Сформировано {PRESENCE} сообщение от {account_name}.')
        return (presense_dict, hash_client_passwd_str)

    # @Log()
    # @staticmethod
    def pars_response_from_server(self, response):
        client_logger.info(f'Разбор сообщения от сервера.')
        if RESPONSE in response:
            if response[RESPONSE] == 200:
                return '200 : OK'
            elif response[RESPONSE] == 511:
                return f'511: {response[DATA]}'
            elif response[RESPONSE] == 400:
                return f'400 : {response[ERROR]}'
            else:
                client_logger.error(
                    f'Принят неизвестный код подтверждения {response[RESPONSE]}')

        elif ACTION in response and response[ACTION] == MESSAGE and SENDER in response and 'to' in response \
                and MESSAGE_TEXT in response and response['to'] == self.client_name:
            client_logger.debug(
                f'Получено сообщение от пользователя {response[SENDER]}:{response[MESSAGE_TEXT]}')
            self.new_message.emit(response)

    def send_message_to_user(self, to_user, message):
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.client_name,
            'to': to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        client_logger.debug(
            f'Сформирован словарь сообщения: {message_dict} для отправки клиенту {to_user}')

        with sock_lock:
            try:
                send_message(self.socket, message_dict)
                client_logger.info(
                    f'Отправлено сообщение для пользователя {to_user}')
            except OSError as err:
                if err.errno:
                    client_logger.critical('Потеряно соединение с сервером.')
                    exit(1)
                else:
                    client_logger.error(
                        'Не удалось передать сообщение. Таймаут соединения')

    # @Log()
    def exit_message(self, account_name):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: account_name
        }

    def print_help(self):
        print('Список команд:')
        print('message - отправить сообщение.')
        print('history - история сообщений')
        print('contacts - список контактов')
        print('edit - редактирование списка контактов')
        print('help - справка по командам')
        print('exit - выход из программы')

    @staticmethod
    def arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-n', '--name', default=None, nargs='?')
        parser.add_argument('-p', '--password', default='', nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        server_address = namespace.addr
        server_port = namespace.port
        client_name = namespace.name
        client_password = namespace.password

        if not 1023 < server_port < 65536:
            client_logger.critical(
                f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
                f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
            sys.exit(1)
        return server_address, server_port, client_name, client_password

    def edit_contacts(self):
        ans = input('Для удаления введите del, для добавления add: ')
        if ans == 'del':
            edit_user = input('Введите имя удаляемного контакта: ')
            with database_lock:
                if self.database.check_contact(edit_user):
                    self.database.del_contact(edit_user)
                else:
                    client_logger.error(
                        'Попытка удаления несуществующего контакта.')
        elif ans == 'add':
            # Проверка на возможность такого контакта
            edit_user = input('Введите имя создаваемого контакта: ')

            if self.database.check_user(edit_user):
                with database_lock:
                    self.database.add_contact(edit_user)
                with sock_lock:
                    try:
                        self.add_contact(edit_user)
                    except BaseException:
                        client_logger.error(
                            'Не удалось отправить информацию на сервер.')

    def print_history(self):
        ask = input(
            'Показать входящие сообщения - in, исходящие - out, все - просто Enter: ')
        with database_lock:
            if ask == 'in':
                history_list = self.database.get_history(
                    to_who=self.client_name)
                for message in history_list:
                    print(
                        f'\nСообщение от пользователя: {message[0]} от {message[3]}:\n{message[2]}')
            elif ask == 'out':
                history_list = self.database.get_history(
                    from_who=self.client_name)
                for message in history_list:
                    print(
                        f'\nСообщение пользователю: {message[1]} от {message[3]}:\n{message[2]}')
            else:
                history_list = self.database.get_history()
                for message in history_list:
                    print(
                        f'\nСообщение от пользователя: {message[0]}, пользователю {message[1]} от {message[3]}\n{message[2]}')

    def add_contact(self, contact):
        client_logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.client_name,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.socket, req)
            ans = receiving_message(self.socket)
        if RESPONSE in ans and ans[RESPONSE] == 200:
            pass
        else:
            raise ValueError('Ошибка создания контакта')
        print('Удачное создание контакта.')

    def del_contact(self, username, contact):
        client_logger.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: DELETE_CONTACT,
            # TIME: time.time(),
            USER: username,
            ACCOUNT_NAME: contact
        }
        send_message(self.socket, req)
        ans = receiving_message(self.socket)
        if RESPONSE in ans and ans[RESPONSE] == 200:
            pass
        else:
            raise ValueError('Ошибка удаления контакта')
        print('Удачное удаление контакта.')

    def contact_list_request(self):
        client_logger.debug(
            f'Запрос контакт листа для пользователся {self.client_name}')
        request = {
            ACTION: CONTACT_LIST,
            TIME: time.time(),
            USER: self.client_name
        }
        client_logger.debug(f'Сформирован запрос {request}')
        with sock_lock:
            send_message(self.socket, request)
            ans = receiving_message(self.socket)
        client_logger.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[DATA_LIST]:
                self.database.add_contact(contact)
        else:
            raise ValueError

    def user_list_request(self):
        client_logger.debug(
            f'Запрос списка известных пользователей {self.client_name}')
        request = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.client_name
        }
        with sock_lock:
            send_message(self.socket, request)
            ans = receiving_message(self.socket)
            print(ans)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[DATA_LIST])
        else:
            raise ServerError


# def database_load(sock, database, username):
#     try:
#         users_list = user_list_request(sock, username)
#     except ServerError:
#         client_logger.error('Ошибка запроса списка известных пользователей.')
#     else:
#         database.add_users(users_list)
#
#     try:
#         contact_list = contact_list_request(sock, username)
#     except:
#         client_logger.error('Ошибка запроса списка контактов.')
#     else:
#         for contact in contact_list:
#             database.add_contact(contact)


def main():
    server_addr, server_port, client_name, client_password = Client.arg_parser()

    app = QApplication(sys.argv)

    start_dialog = UserNameDialog()
    if not client_name or not client_password:
        # client_name = input('Введите имя пользователя: ')
        app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_password = start_dialog.client_passwd.text()
            client_logger.debug(
                f'Using USERNAME = {client_name}, PASSWD = {client_password}.')
        else:
            exit(0)

    # dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        # генерация ключа RSA
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            # генерация приватного ключа
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    database = ClientDatabase(client_name)
    # database_load(client_socket, database, client_name)

    client = Client(
        server_addr,
        server_port,
        client_name,
        database,
        client_password,
        keys)
    client.setDaemon(True)
    client.start()

    client_logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_addr} , порт: {server_port}, имя пользователя: {client_name}')

    del start_dialog
    # try:
    #     # сообщение о присутствии на сервер
    #     send_message(client.socket, client.generating_presence_message(client_name))
    #     response = Client.pars_response_from_server(receiving_message(client.socket))
    #     # print(response)
    #     if RESPONSE in response:
    #         if response[RESPONSE] == 400:
    #             raise ServerError(response[ERROR])
    #         elif response[RESPONSE] == 511:
    #             response_data = response[DATA]
    #             hash = hmac.new(client.generating_presence_message(client_name)[USER][PASSWORD], response_data.encode('utf-8'), 'MD5')
    #             digest = hash.digest()
    #             my_ans = RESPONSE_511
    #             my_ans[DATA] = binascii.b2a_base64(digest).decode('ascii')
    #             send_message(client.socket, my_ans)
    #             client.message_from_server()
    # except (OSError, json.JSONDecodeError) as err:
    #     client_logger.debug(f'Connection error.', exc_info=err)
    #     raise ServerError('Сбой соединения в процессе авторизации.')
    #
    # # database_load(client.socket, database, client_name)
    #
    # client_logger.info(f'Соединение с сервером установлено. Ответ сервера: {response}')

    window = MainWindowClient(database, client, keys)
    window.setWindowTitle(f'Мессенджер. {client_name}')
    window.statusBar().showMessage('Соединение с сервером установлено.')
    window.make_connection(client)

    client_logger.debug('Процессы приема и передачи сообщений запущены.')

    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

    # app = QApplication(sys.argv)
    # window = MainWindowClient()
    # client_name = 'user_1'
    # window.setWindowTitle(f'Мессенджер. {client_name}')
    # window.statusBar().showMessage('Соединение с сервером установлено.')
    # window.show()
    # sys.exit(app.exec_())
