# Логика работы с БД (запросы)

import mysql.connector
from mysql.connector import Error

# Функция для создания подключения
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Адрес сервера базы данных
            database="shop",   # Название базы данных
            user="root",       # Имя пользователя
            password="mysql123" # Пароль
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None