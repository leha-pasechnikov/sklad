from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Настройки подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sklad'
}

# Подключение к базе данных
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Главная страница с отображением товаров
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_перечень_товаров, наименование, `штрих-код` FROM `перечень товаров`")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Обработчик покупки товара
@app.route('/buy/<int:product_id>', methods=['POST'])
def buy_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Добавляем запрос для обновления или вставки данных о покупке

    cursor.execute("INSERT INTO заказ (`время_на_сборку`, `время_сборки`, `время_проверки`, `время_отправки`, `статус`, `клиент_id_клиент`, `менеджер_id_менеджер`, `камера_хранения_заказа_id_место_оформления_заказа`, `проверяющий комплектовку_id_проверяющий_комплектовку`, `комплектовщик_id_комплектовщик`,`водитель_id_водитель`) VALUES ('2024-09-27 20:00:00', '2024-09-27 18:23:01', '2024-09-27 18:43:45', '2024-09-27 18:53:55', 'пример', 3, 1, 5, 1, 1,2);")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
