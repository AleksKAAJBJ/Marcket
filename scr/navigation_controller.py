class NavigationController:
    def __init__(self, ui, category_controller=None):
        """
        Контроллер навигации между страницами.

        :param ui: Ссылка на UI.
        :param category_controller: Контроллер категорий для загрузки данных.
        """
        self.ui = ui
        self.category_controller = category_controller

    def go_to_page_shop(self):
        """Переключение на страницу магазина"""
        self.ui.stackedWidget.setCurrentIndex(2)
        if self.category_controller:
            self.category_controller.load_categories_and_subcategories()

    def go_to_login_page(self):
        """Переключение на страницу входа"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def go_to_register_page(self):
        """Переключиться на страницу регистрации"""
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_orders_page(self):
        """Переключиться на страницу заказов"""
        self.ui.stackedWidget.setCurrentIndex(3)

    def go_to_cart_page(self):
        """Переключиться на страницу корзины"""
        self.ui.stackedWidget.setCurrentIndex(4)

    def go_to_personal_account(self):
        """Переключиться на страницу личного кабинета"""
        self.ui.stackedWidget.setCurrentIndex(5)
