# Определение моделей БД (таблицы)

import bcrypt
import mysql.connector
from mysql.connector import IntegrityError, Error
from db.database import create_connection

# Функция для проверки пользователя
def check_user(phone, password):
    """Проверка наличия пользователя с таким номером телефона и паролем"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE phone = %s"
        cursor.execute(query, (phone,))
        user = cursor.fetchone()

        # Закрываем соединение с БД
        cursor.close()
        connection.close()

        if user:
            # Проверяем, соответствует ли пароль
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return user['id_user']
        return None
    return None

# Функция для создания нового пользователя
def create_user(first_name, password, email, phone):
    """Создание нового пользователя"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

        # Хешируем пароль перед сохранением
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Запрос на добавление пользователя в базу данных
        query = "INSERT INTO users (first_name, password, email, phone) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (first_name, hashed_password, email, phone))
            connection.commit()
            cursor.close()
            connection.close()
            return True, None  # Успешная регистрация
        except mysql.connector.errors.IntegrityError as e:
            # Проверяем, какая именно ошибка уникальности произошла
            if "Duplicate entry" in str(e):
                if "email" in str(e):
                    return False, "Этот email уже зарегистрирован."
                elif "phone" in str(e):
                    return False, "Этот номер телефона уже зарегистрирован."
            return False, "Произошла ошибка при регистрации пользователя."
        except Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False, "Произошла ошибка при регистрации пользователя."
        finally:
            cursor.close()
            connection.close()
    return False, "Не удалось подключиться к базе данных."

def get_user_data(user_id):
    """Получить данные пользователя по его ID"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id_user = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        # Закрываем соединение с БД
        cursor.close()
        connection.close()

        if user_data:
            return user_data
        else:
            return None
    return None

# Функция для получения всех категорий
def get_categories():
    """Получить все категории из базы данных"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM categories"
        cursor.execute(query)
        categories = cursor.fetchall()

        cursor.close()
        connection.close()
        return categories
    return []

# Функция для получения подкатегорий по ID категории
def get_subcategories_by_category(category_id):
    """Получить все подкатегории для данной категории"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM subcategories WHERE id_category = %s"
        cursor.execute(query, (category_id,))
        subcategories = cursor.fetchall()

        cursor.close()
        connection.close()
        return subcategories
    return []

def get_products_by_subcategory(subcategory_id):
    """Получить все товары для подкатегории"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM products WHERE id_subcategory = %s"
        cursor.execute(query, (subcategory_id,))
        products = cursor.fetchall()

        cursor.close()
        connection.close()
        return products
    return []

def get_subcategory_id_by_name(subcategory_name):
    """Получить ID подкатегории по её названию"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id_subcategory FROM subcategories WHERE name = %s"
        cursor.execute(query, (subcategory_name,))
        subcategory = cursor.fetchone()

        cursor.close()
        connection.close()
        if subcategory:
            return subcategory['id_subcategory']
    return None
