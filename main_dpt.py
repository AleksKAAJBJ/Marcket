from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem

class ProductDetailsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Детали товара")
        self.setGeometry(100, 100, 600, 400)

        # Создаем TabWidget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Добавляем вкладки
        self.tab_widget.addTab(self.create_description_tab(), "Описание")
        self.tab_widget.addTab(self.create_characteristics_tab(), "Характеристики")

    def create_description_tab(self):
        """Создает вкладку с описанием товара"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Пример описания
        description_label = QLabel("Описание товара:")
        description_content = QLabel(
            "Это качественный и надежный товар. Он отлично подходит для повседневного использования и обладает следующими преимуществами:\n\n"
            "- Высокая производительность\n"
            "- Привлекательный дизайн\n"
            "- Длительный срок службы"
        )
        description_content.setWordWrap(True)

        # Добавляем элементы на вкладку
        layout.addWidget(description_label)
        layout.addWidget(description_content)

        return tab

    def create_characteristics_tab(self):
        """Создает вкладку с характеристиками товара"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Пример таблицы характеристик
        table = QTableWidget()
        table.setColumnCount(2)  # Две колонки: Название и Значение
        table.setRowCount(4)  # Четыре строки для примера
        table.setHorizontalHeaderLabels(["Характеристика", "Значение"])
        table.setItem(0, 0, QTableWidgetItem("Цвет"))
        table.setItem(0, 1, QTableWidgetItem("Черный"))
        table.setItem(1, 0, QTableWidgetItem("Вес"))
        table.setItem(1, 1, QTableWidgetItem("1.5 кг"))
        table.setItem(2, 0, QTableWidgetItem("Мощность"))
        table.setItem(2, 1, QTableWidgetItem("200 Вт"))
        table.setItem(3, 0, QTableWidgetItem("Материал"))
        table.setItem(3, 1, QTableWidgetItem("Металл"))

        # Настройки таблицы
        table.resizeColumnsToContents()
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Запрет на редактирование

        # Добавляем таблицу на вкладку
        layout.addWidget(table)

        return tab


if __name__ == "__main__":
    app = QApplication([])
    window = ProductDetailsWindow()
    window.show()
    app.exec_()
