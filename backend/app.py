from flask import Flask, render_template, request, redirect, url_for
import mysql.connector  # Импортируем правильный модуль для работы с MySQL

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Замените на ваш хост
        user="root",  # Замените на ваше имя пользователя
        password="",  # Замените на ваш пароль
        database="sklad"  # Название базы данных
    )

# Функция для загрузки данных (SELECT)
def load_data_from_db(query):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения данных
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Функция для модифицирующих запросов (INSERT, UPDATE, DELETE)
def modify_db(query, params):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Выполняем SQL-запрос для изменения данных
    cursor.execute(query, params)
    conn.commit()
    conn.close()

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Добавление новой записи в базу данных
@app.route('/add', methods=['POST'])
def add_record():
    if request.method == 'POST':
        # Запрос на вставку данных
        query = '''
        INSERT INTO `перечень товаров` (id_перечень_товаров, наименование, `штрих-код`)
        VALUES (%s, %s, %s)
        '''
        params = (1000, 'sds', '2321323123123131231231232')

        # Выполняем запрос на изменение (вставка)
        modify_db(query, params)

        # Перенаправление на главную страницу
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
