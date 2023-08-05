import base64
import json
import logging

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from client.add_contact import AddContactDialog
from client.client_gui import Ui_MainWindowClient
from common.errors import ServerError
from common.settings import MESSAGE_TEXT, SENDER, DESTINATION

client_logger = logging.getLogger('client')


class MainWindowClient(QMainWindow):
    def __init__(self, database, client, keys):
        QMainWindow.__init__(self)

        self.database = database
        self.client = client

        self.contact_model = QStandardItemModel()
        self.message_history_model = QStandardItemModel()
        self.current_contact = None
        self.current_contact_key = None
        self.messages = QMessageBox()

        self.decrypter = PKCS1_OAEP.new(keys)
        self.encryptor = None

        self.ui = Ui_MainWindowClient()
        self.ui.setupUi(self)

        self.ui.listView_contacts.doubleClicked.connect(self.start_chat)

        self.ui.Button_add_contact.clicked.connect(self.add_contact_window)
        self.ui.Button_del_contact.clicked.connect(self.del_contact)

        self.ui.Button_clear.clicked.connect(self.clear_message)
        self.ui.Button_send.clicked.connect(self.send_message)

        self.ui.Button_clear.setDisabled(True)
        self.ui.Button_send.setDisabled(True)
        self.ui.textEdit_message.setDisabled(True)

        self.update_contact_list()
        self.show()

    def update_contact_list(self):
        self.contact_model.clear()
        contact_list = self.database.get_contacts()
        contact_list = sorted(contact_list)
        for contact in contact_list:
            contact_item = QStandardItem(contact)
            contact_item.setEditable(False)
            # contact_item.setBackground(QColor(0, 255, 255, 255))
            self.contact_model.appendRow(contact_item)
        self.ui.listView_contacts.setModel(self.contact_model)

    def start_chat(self):
        # self.message_history_model.clear()
        self.current_contact = self.ui.listView_contacts.currentIndex().data()
        # self.load_history_chat()
        for i in range(self.contact_model.rowCount()):
            if self.contact_model.item(i).text() == self.current_contact:
                self.contact_model.item(i).setBackground(
                    QColor(255, 255, 255, 255))

        try:
            self.current_contact_key = self.client.key_request(
                self.current_contact)

            client_logger.debug(
                f'Загружен открытый ключ для {self.current_contact}')
            if self.current_contact_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_contact_key))
        except (OSError, json.JSONDecodeError):
            self.current_contact_key = None
            self.encryptor = None
            client_logger.debug(
                f'Не удалось получить ключ для {self.current_contact}')

        if not self.current_contact_key:
            self.messages.warning(
                self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return

        self.ui.Button_clear.setEnabled(True)
        self.ui.Button_send.setEnabled(True)
        self.ui.textEdit_message.setEnabled(True)

        self.ui.label_message.setText(f'Введите сообщение для {self.current_contact}:')

        self.load_history_chat()

    def load_history_chat(self):
        self.message_history_model.clear()
        message_list = self.database.get_history(
            self.client.client_name, self.current_contact)
        # print(message_list)
        message_list = sorted(message_list, key=lambda item: item[3])

        for message in message_list:
            message_item = QStandardItem(f'{message[3]}:\n{message[2]}')
            message_item.setEditable(False)
            if message[0] == self.current_contact:
                message_item.setTextAlignment(Qt.AlignLeft)
            else:
                message_item.setTextAlignment(Qt.AlignRight)
            self.message_history_model.appendRow(message_item)
        self.ui.listView_history.setModel(self.message_history_model)

    def add_contact_window(self):
        # global select_dialog
        select_dialog = AddContactDialog(self.client, self.database)
        select_dialog.btn_ok.clicked.connect(
            lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        new_contact = item.selector.currentText()
        self.client.add_contact(new_contact)
        new_contact = QStandardItem(new_contact)
        new_contact.setEditable(False)
        self.contact_model.appendRow(new_contact)
        item.close()

    def del_contact(self):
        self.current_contact = self.ui.listView_contacts.currentIndex().data()
        self.client.del_contact(self.client.client_name, self.current_contact)
        self.update_contact_list()

    def clear_message(self):
        self.ui.textEdit_message.clear()

    def send_message(self):
        message = self.ui.textEdit_message.toPlainText()
        # if message:
        #     self.client.send_message_to_user(self.current_contact, message)
        #     self.load_history_chat()
        #     self.ui.textEdit_message.clear()
        # else:
        #     return

        message_text_encrypted = self.encryptor.encrypt(message.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)
        try:
            self.client.send_message_to_user(
                self.current_contact,
                message_text_encrypted_base64.decode('ascii'))
        except ServerError as err:
            self.messages.critical(self, 'Ошибка', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(
                    self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(
                self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.save_message(
                self.client.client_name, self.current_contact, message)
            client_logger.debug(
                f'Отправлено сообщение для {self.current_contact}: {message}')
            self.load_history_chat()
            self.clear_message()

    @pyqtSlot(dict)
    def message(self, message):
        encrypted_message = base64.b64decode(message[MESSAGE_TEXT])

        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
            # decrypted_message = message[MESSAGE_TEXT]
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return

        # self.database.save_message(self.current_contact, 'in', decrypted_message.decode('ascii'))
        self.database.save_message(
            message[SENDER],
            message[DESTINATION],
            decrypted_message.decode('utf8'))

        sender = message[SENDER]
        if sender == self.current_contact:
            self.load_history_chat()
        else:
            if not self.database.check_contact(sender):
                self.add_contact_action(sender)
            for i in range(self.contact_model.rowCount()):
                if self.contact_model.item(i).text() == sender:
                    self.contact_model.item(i).setBackground(
                        QColor(0, 0, 255, 255))

    @pyqtSlot()
    def connection_lost(self):
        self.messages.warning(
            self,
            'Сбой соединения',
            'Потеряно соединение с сервером. ')
        self.close()

    def make_connection(self, client_obj):
        client_obj.new_message.connect(self.message)
        client_obj.connection_lost.connect(self.connection_lost)
