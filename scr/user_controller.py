import re
from db.models import check_user, create_user, get_user_data
from scr.category_controller import Category_controller
from scr.navigation_controller import NavigationController
from PyQt5.QtWidgets import QMessageBox

class User_controller:
    def __init__(self, ui):
        self.ui = ui  # Привязка UI к контроллеру
        self.current_user_id = None  # ID текущего пользователя
        self.category_controller = Category_controller(self.ui)  # Создание экземпляра Category_controller
        self.navigation = NavigationController(self.ui, self.category_controller)  # Создание экземпляра NavigationController

    def handle_signin(self):
        """Обработчик кнопки входа"""
        phone = self.ui.lineEdit_phone.text()
        password = self.ui.lineEdit_psw.text()

        # Валидация телефона
        if not phone or not phone.isdigit() or len(phone) != 11:
            self.show_error("Неверный номер телефона!")
            return

        # Валидация пароля
        if not password or len(password) < 8:
            self.show_error("Пароль должен быть не менее 8 символов!")
            return

        # Проверка в базе данных
        user_id = check_user(phone, password)
        if user_id:
            self.current_user_id = user_id  # Сохраняем ID пользователя
            self.navigation.go_to_page_shop()  # Переключаемся на страницу магазина
        else:
            self.show_error("Неверный телефон или пароль!")

    def handle_signup(self):
        """Обработчик кнопки регистрации"""
        first_name = self.ui.lineEdit_name.text()
        password = self.ui.lineEdit_psw_2.text()
        email = self.ui.lineEdit_email.text()
        phone = self.ui.lineEdit_phone_2.text()

        # Валидация данных
        if not first_name or not phone or not email or not password:
            self.show_error("Пожалуйста, заполните все поля!")
            return

        if len(phone) != 11 or not phone.isdigit():
            self.show_error("Неверный формат номера телефона!")
            return

        if len(password) < 6:
            self.show_error("Пароль должен быть не менее 6 символов!")
            return

        # Валидация email
        email_regex = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|mail\.ru)$'
        if not re.match(email_regex, email):
            self.show_error("Неверный формат email! Используйте gmail.com или mail.ru.")
            return

            # Создание нового пользователя
        success, message = create_user(first_name, password, email, phone)
        if success:
            self.show_success("Регистрация прошла успешно!")
        
            # Получаем user_id после регистрации
            self.current_user_id = check_user(phone, password)  # Проверяем пользователя по телефону и паролю
            if self.current_user_id:
                self.show_success("Добро пожаловать!")
            else:
                self.show_error("Ошибка при получении ID пользователя!")
        else:
            self.show_error(message)

    def handle_personal_account_button(self):
        """Обработчик кнопки 'Личный кабинет'"""
        if self.current_user_id:
            self.update_personal_account()  # Обновляем данные личного кабинета
            self.navigation.go_to_personal_account()  # Переход на страницу личного кабинета
        else:
            self.show_error("Вы не авторизованы!")

    def update_personal_account(self):
        """Обновление информации в личном кабинете"""
        if self.current_user_id:
            user_data = get_user_data(self.current_user_id)
            if user_data:
                self.ui.lineEdit_name_2.setText(user_data.get("first_name", ""))
                self.ui.lineEdit_email_2.setText(user_data.get("email", ""))
                self.ui.lineEdit_phone_3.setText(user_data.get("phone", ""))

    def show_error(self, message):
        """Отображение окна с ошибкой"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def show_success(self, message):
        """Отображение окна с успешным сообщением"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Успех")
        msg.exec_()
