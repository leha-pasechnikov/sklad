import tkinter as tk
from tkinter import messagebox
import mysql.connector
from main import main


# Подключение к базе данных MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Замените на ваш хост
        user="root",  # Замените на ваше имя пользователя
        password="",  # Замените на ваш пароль
        database="sklad"  # Название базы данных
    )


# Функция для загрузки данных из таблицы 'заказ'
def load_data_from_db(query):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения данных из таблицы 'заказ'
    cursor.execute(query)

    # Получаем все строки из результата запроса
    rows = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return rows


def check_login():
    username = entry_username.get()
    password = entry_password.get()

    # Проверка логина и пароля
    user = load_data_from_db(f'SELECT * FROM сотрудник WHERE логин = "{username}" AND пароль = "{password}" AND (специальность = "менеджер" OR специальность = "начальник смены");')

    if user:

        messagebox.showinfo("Вход", f"Здравствуйте, {user[0][6]} {user[0][7]} {user[0][8]}!")
        login_window.destroy()  # Закрываем окно входа
        main(int(user[0][0]))  # Открываем основное окно
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")


def open_login_window():
    global entry_username, entry_password, login_window

    # Создаем окно для входа
    login_window = tk.Tk()
    login_window.title("Вход")
    login_window.geometry("300x200+800+400")

    # Метка и поле ввода для логина
    label_username = tk.Label(login_window, text="Логин:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    # Метка и поле ввода для пароля
    label_password = tk.Label(login_window, text="Пароль:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    # Кнопка для входа
    button_login = tk.Button(login_window, text="Войти", command=check_login)
    button_login.pack(pady=10)

    login_window.mainloop()


# Запуск окна входа
open_login_window()
