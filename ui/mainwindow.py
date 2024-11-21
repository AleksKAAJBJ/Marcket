import sys
import os

# Добавляем путь к папке 'scr' в список путей поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Теперь можно импортировать из 'scr.controllers'
from scr.user_controller import User_controller
from scr.category_controller import Category_controller
from scr.navigation_controller import NavigationController
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_MainWindow import Ui_Shop

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Shop()
        self.ui.setupUi(self)

        # Создаём экземпляры контроллеров
        self.Category_controller = Category_controller(self.ui)
        self.Navigation = NavigationController(self.ui, self.Category_controller)  # Навигационный контроллер
        self.User_controller = User_controller(self.ui)

        # Устанавливаем начальный индекс
        self.ui.stackedWidget.setCurrentIndex(0)
        

        # Привязываем кнопки к методам
        self.ui.btn_signin.clicked.connect(self.User_controller.handle_signin)
        self.ui.btn_signup_2.clicked.connect(self.Navigation.go_to_register_page)

        # Кнопки на странице регистрации (индекс 1)
        self.ui.btn_signup.clicked.connect(self.User_controller.handle_signup)
        self.ui.btn_signin_2.clicked.connect(self.Navigation.go_to_login_page)

        # Кнопки на странице магазина (индекс 2)
        self.ui.btn_orders.clicked.connect(self.Navigation.go_to_orders_page)
        self.ui.btn_cart.clicked.connect(self.Navigation.go_to_cart_page)
        self.ui.btn_pers_acc.clicked.connect(self.User_controller.handle_personal_account_button)

        # Кнопка "Вернуться назад" на странице "Заказы" (индекс 3)
        self.ui.btn_orders_shop.clicked.connect(self.Navigation.go_to_page_shop)

        # Кнопка "Оформить заказ" на странице "Корзина" (индекс 4)
        self.ui.btn_orders_cart.clicked.connect(self.Navigation.go_to_orders_page)

        # Кнопка "В магазин" на странице с индексом 5 (Личный кабинет)
        self.ui.btn_pers_acc_shop.clicked.connect(self.Navigation.go_to_page_shop)

        # Связывает кнопку "Личный кабинет" с обработчиком нажатия.
        # Метод handle_personal_account_button проверяет авторизацию и открывает личный кабинет.
        self.ui.btn_pers_acc.clicked.connect(self.User_controller.handle_personal_account_button)

        self.ui.treeWidget_category.itemClicked.connect(self.Category_controller.on_subcategory_selected)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())