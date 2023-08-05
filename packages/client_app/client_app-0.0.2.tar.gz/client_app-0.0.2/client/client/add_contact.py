
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton

client_logger = logging.getLogger('client')


class AddContactDialog(QDialog):
    def __init__(self, client, database):
        super().__init__()
        self.client = client
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.possible_contacts_update()

        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        self.selector.clear()
        # множества всех контактов и контактов клиента
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())
        # Удалим сами себя из списка пользователей, чтобы нельзя было добавить
        # самого себя
        users_list.remove(self.client.client_name)
        # Добавляем список возможных контактов
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        try:
            self.client.user_list_request()
        except OSError:
            pass
        else:
            client_logger.debug(
                'Обновление списка пользователей с сервера выполнено')
            self.possible_contacts_update()
