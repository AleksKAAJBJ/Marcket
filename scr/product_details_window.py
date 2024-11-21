from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap
from db.models import get_products_by_subcategory, get_subcategory_id_by_name


class ProductDetailWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.productGridWidget = QWidget(self)  # Здесь будут кнопки с изображениями
        self.grid_layout = QGridLayout(self.productGridWidget)
        self.layout.addWidget(self.productGridWidget)
    
    def fill_product_details(self, product):
        """Заполнение UI данными товара"""
        self.label_name_product.setText(product['model_name'])
        self.label_input_price.setText(f"${product['price']}")
        self.label_2.setText(product['description'])
        
        # Дополнительные данные товара
        self.fill_product_characteristics(product['id_product'])  # Заполнение характеристик
    
    def fill_product_characteristics(self, product_id):
        """Заполняем характеристики товара в таблице"""
        query = """
        SELECT characteristic_name, characteristic_value
        FROM product_characteristics
        WHERE id_product = %s
        """
        result = get_product_characteristics(product_id)
        characteristics = result.fetchall()  # Получаем все строки

        self.tableWidget_tab.setRowCount(0)  # Очищаем таблицу перед заполнением

        for row, characteristic in enumerate(characteristics):
            self.tableWidget_tab.insertRow(row)  # Добавляем строку
            self.tableWidget_tab.setItem(row, 0, QtWidgets.QTableWidgetItem(characteristic['characteristic_name']))
            self.tableWidget_tab.setItem(row, 1, QtWidgets.QTableWidgetItem(characteristic['characteristic_value']))

    def show_product_details(self, product_id):
        """Метод для отображения подробной информации о товаре"""
        product = get_product_details(product_id)
        self.fill_product_details(product)
        self.stackedWidget.setCurrentIndex(6)  # Переключение на страницу с деталями товара

    def get_product_details(self, product_id):
        """Получаем подробности товара из базы данных"""
        query = "SELECT * FROM products WHERE id_product = %s"
        result = db.execute(query, (product_id,))
        return result.fetchone()  # Возвращаем первую строку с данными товара