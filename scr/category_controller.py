from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidgetItem, QLabel, QPushButton, QVBoxLayout, QMessageBox, QWidget, QGridLayout
from db.models import get_categories, get_subcategories_by_category, get_products_by_subcategory, get_subcategory_id_by_name

class Category_controller():
    def __init__(self, ui):
        self.ui = ui  # Привязка UI к контроллеру

        self.productGridWidget = self.ui.productGridWidget
        self.productGridWidget.setLayout(QVBoxLayout())  # Инициализация layout для кнопок с товарами

    def clear_layout(self, widget):
        """Очищаем текущий layout в widget перед добавлением нового."""
        current_layout = widget.layout()
        if current_layout:
            # Удаляем старый layout
            for i in reversed(range(current_layout.count())):
                widget_to_remove = current_layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.deleteLater()
            # Затем удаляем сам layout
            widget.setLayout(None)  # Убираем текущий layout


    def show_error(self, message):
        """Отображение окна с ошибкой"""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setText(message)
        error_dialog.exec_()

    def load_categories_and_subcategories(self):
        """Загрузка категорий и подкатегорий в TreeWidget"""
        categories = get_categories()

        # Очищаем старые данные в TreeWidget перед добавлением новых
        self.ui.treeWidget_category.clear()

        # Устанавливаем заголовки для TreeWidget
        self.ui.treeWidget_category.setHeaderLabels(["Каталог"])

        for category in categories:
            # Создаем основной элемент категории
            category_item = QTreeWidgetItem(self.ui.treeWidget_category)
            category_item.setText(0, category['name'])

            # Получаем подкатегории для этой категории
            subcategories = get_subcategories_by_category(category['id_category'])

            for subcategory in subcategories:
                # Создаем подкатегорию как дочерний элемент
                subcategory_item = QTreeWidgetItem(category_item)
                subcategory_item.setText(0, subcategory['name'])

    def on_subcategory_selected(self, item, column):
        """Обработчик нажатия на подкатегорию"""
        # Получаем название подкатегории
        subcategory_name = item.text(0)

        # Получаем ID подкатегории из базы данных по её названию
        subcategory_id = self.get_subcategory_id_by_name(subcategory_name)

        # Проверка на пустое значение
        if not subcategory_id:
            self.show_error("ID подкатегории пустое.")
            return

        # Получаем товары, связанные с подкатегорией
        products = get_products_by_subcategory(subcategory_id)

        # Очищаем старые элементы в gridLayout
        self.clear_layout(self.productGridWidget)

        # Отображаем товары в gridLayout
        self.display_products(products)

    def display_product_button(self, product):
        """Создает кнопку для товара и добавляет её в layout."""
        button = QPushButton(f"{product['model_name']} - {product['price']} ₽")
        button.setStyleSheet("background-color: #f5f5f5; border: 1px solid #654321; border-radius: 5px;")
        self.productGridWidget.layout().addWidget(button)

        # Установка изображения на кнопку
        if product.get('image_url'):
            pixmap = QPixmap(product['image_url'])
            button.setIcon(pixmap)
            button.setIconSize(pixmap.size())

        # Подключение обработчика нажатия
        button.clicked.connect(lambda: self.show_product_details(product))

    def show_product_details(self, product):
        """Отображение деталей товара."""
        self.ui.stackedWidget.setCurrentIndex(6)  # Открываем страницу с деталями
        self.ui.label_name_product.setText(product['model_name'])
        self.ui.label_input_price.setText(f"{product['price']} ₽")
        self.ui.label_2.setText(product.get('description', 'Нет описания'))

        # Отображение изображения
        if product.get('image_url'):
            pixmap = QPixmap(product['image_url'])
            self.ui.label_image.setPixmap(pixmap.scaled(341, 291))
        else:
            self.ui.label_image.setText("Изображение отсутствует")