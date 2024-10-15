from flask import Flask, render_template, url_for, jsonify, request
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)


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


def save_data_to_bd(quary: list):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host="localhost",  # Замените на ваш хост
            user="root",  # Замените на ваше имя пользователя
            password="",  # Замените на ваш пароль
            database="sklad"  # Название базы данных
        )
        cursor = conn.cursor()

        for i in quary:
            if type(i) == str:
                cursor.execute(i)
            elif type(i) == list:
                for j in i:
                    cursor.execute(j)

        conn.commit()
    except mysql.connector.Error as error:
        print(error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_tovar_food', methods=['GET'])
def get_tovar_food():
    try:
        data = load_data_from_db('''
SELECT 
    z.наименование,z.`ссылка на изображение`, z.цена,
    COUNT(*) AS count
FROM 
    `перечень товаров` z
JOIN 
    товар s ON s.`перечень товаров_id_перечень_товаров` = z.id_перечень_товаров 
where s.статус="свободен" and z.категория_id_категория=1  
GROUP BY 
    наименование,`ссылка на изображение`, цена        
        ''')
        return jsonify(data)
    except:
        return jsonify({'error': str(err)}), 500


@app.route('/get_tovar_clothes', methods=['GET'])
def get_tovar_clothes():
    try:
        data = load_data_from_db('''
SELECT 
    z.наименование,z.`ссылка на изображение`, z.цена,
    COUNT(*) AS count
FROM 
    `перечень товаров` z
JOIN 
    товар s ON s.`перечень товаров_id_перечень_товаров` = z.id_перечень_товаров 
where s.статус="свободен" and z.категория_id_категория=2  
GROUP BY 
    наименование,`ссылка на изображение`, цена        
                ''')
        print(jsonify(data))
        return jsonify(data)
    except:
        return jsonify({'error': str(err)}), 500


@app.route('/get_tovar_toys', methods=['GET'])
def get_tovar_toys():
    try:
        data = load_data_from_db('''
SELECT 
    z.наименование,z.`ссылка на изображение`, z.цена,
    COUNT(*) AS count
FROM 
    `перечень товаров` z
JOIN 
    товар s ON s.`перечень товаров_id_перечень_товаров` = z.id_перечень_товаров 
where s.статус="свободен" and z.категория_id_категория=3  
GROUP BY 
    наименование,`ссылка на изображение`, цена        
                ''')
        return jsonify(data)
    except:
        return jsonify({'error': str(err)}), 500


@app.route('/add_zakaz', methods=['POST', 'GET'])
def add_zakaz():
    if request.method == "POST":
        id_client = 1  # request.form['id_client']
        values = {'Молоко': 2, 'Хлеб': 1}  # список товаров в заказе
        try:
            # Получение последнего ID заказа
            last_id_query = 'SELECT id_заказ FROM заказ ORDER BY id_заказ DESC LIMIT 1'
            id_zakaz = int(load_data_from_db(last_id_query)[0][0]) + 1

            # Получение менеджера
            id_meneger_query = '''
            SELECT id_менеджер 
            FROM менеджер 
            WHERE сотрудник_id_сотрудник = (
                SELECT id_сотрудник
                FROM (
                    SELECT id_сотрудник
                    FROM сотрудник 
                    WHERE специальность = "менеджер"
                    ORDER BY статус, RAND() 
                    LIMIT 1
                ) AS subquery
            );'''
            id_meneger = load_data_from_db(id_meneger_query)[0][0]

            # Получение комплектовщика
            id_komplekt_query = '''
            SELECT id_комплектовщик 
            FROM комплектовщик 
            WHERE сотрудник_id_сотрудник = (
                SELECT id_сотрудник
                FROM (
                    SELECT id_сотрудник
                    FROM сотрудник 
                    WHERE специальность = "комплектовщик"
                    ORDER BY статус, RAND() 
                    LIMIT 1
                ) AS subquery
            );'''
            id_komplekt = load_data_from_db(id_komplekt_query)[0][0]

            # Получение проверяющего
            id_prover_query = '''
            SELECT id_проверяющий_комплектовку 
            FROM `проверяющий комплектовку` 
            WHERE сотрудник_id_сотрудник = (
                SELECT id_сотрудник
                FROM (
                    SELECT id_сотрудник
                    FROM сотрудник 
                    WHERE специальность = "проверяющий комплектовку"
                    ORDER BY статус, RAND() 
                    LIMIT 1
                ) AS subquery
            );'''
            id_prover = load_data_from_db(id_prover_query)[0][0]

            # Получение водителя
            id_vodit_query = '''
            SELECT id_водитель 
            FROM водитель 
            WHERE сотрудник_id_сотрудник = (
                SELECT id_сотрудник
                FROM (
                    SELECT id_сотрудник
                    FROM сотрудник 
                    WHERE специальность = "водитель"
                    ORDER BY статус, RAND() 
                    LIMIT 1
                ) AS subquery
            );'''
            id_vodit = load_data_from_db(id_vodit_query)[0][0]

            # Получение места
            mesto_query = '''
            SELECT id_место_оформления_заказа 
            FROM камера_хранения_заказа 
            ORDER BY статус DESC, RAND() 
            LIMIT 1;'''
            mesto = load_data_from_db(mesto_query)[0][0]

            # Рассчет времени
            time_give = (datetime.now() + timedelta(minutes=len(values) * 15 + 60)).replace(second=0, microsecond=0)

            # Формирование запроса для вставки заказа
            quary_zakaz = f'''
            INSERT INTO заказ (id_заказ, `клиент_id_клиент`, `время_на_сборку`, `время_сборки`, `время_проверки`, 
            `время_отправки`, `статус`, `менеджер_id_менеджер`, `комплектовщик_id_комплектовщик`, 
            `проверяющий комплектовку_id_проверяющий_комплектовку`, `водитель_id_водитель`, 
            `камера_хранения_заказа_id_место_оформления_заказа`) VALUES ({id_zakaz}, {id_client}, "{time_give}", null, null, null, 'готовится к сборке', {id_meneger}, {id_komplekt}, {id_prover}, {id_vodit}, {mesto});'''

            quary_update = []
            quary_tovar = 'INSERT INTO `товары в заказе` (товар_id_товара, статус, заказ_id_заказ) VALUES '

            for key in values:
                id_tovar = load_data_from_db(f'''
                SELECT id_товара 
                FROM товар 
                WHERE `перечень товаров_id_перечень_товаров` = (
                    SELECT id_перечень_товаров 
                    FROM `перечень товаров` 
                    WHERE наименование="{key}"
                ) AND статус="свободен" 
                ORDER BY время_распределения 
                LIMIT {values[key]}''')

                if not id_tovar:
                    continue

                for i in id_tovar:
                    quary_tovar += f'({i[0]},"готовится к сборке",{id_zakaz}),'
                    quary_update.append(f"UPDATE товар SET статус = 'занят' WHERE id_товара = {i[0]};")
            quary_tovar = quary_tovar[:-1] + ';'

            # Выполнение всех запросов
            try:
                save_data_to_bd([quary_zakaz, quary_tovar, quary_update])
                return jsonify({'message': f'Заказ успешно оформлен.\nВашему заказу присвоен номер {id_zakaz}'}), 201
            except Exception as err:
                print(f'Ошибка при сохранении данных: {err}')
                return jsonify({'error': str(err)}), 500
        except Exception as err:
            print(f'Ошибка: {err}')
            return jsonify({'error': str(err)}), 500


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method=="POST":
        familia = 'Иванов'
        ima = 'Иван'
        otchestvo = 'Иванович'
        telefon = '+79161234567'
        pochta = 'ivanov@mail.ru'
        parol = 'pass324'

        try:
            quary = f'''
    INSERT INTO клиент(фамилия, имя, отчество, номер_телефона, почта, пароль) VALUES
    ('{familia}', '{ima}', '{otchestvo}', '{telefon}', '{pochta}', '{parol}')'''
            save_data_to_bd([quary])
            return jsonify({'message': f'Вы успешно зарегистрированы.'}), 201
        except Exception as err:
            return jsonify({'error': str(err)}), 500


@app.route('/user_verification', methods=['POST', 'GET'])
def user_verification():
    if request.method == "POST":
        telefon_or_pochta = '+79161234567'
        parol = 'pass324'
        try:
            data = load_data_from_db(f'''
    select * from клиент where 
    (номер_телефона='{telefon_or_pochta}' or почта='{telefon_or_pochta}') and пароль='{parol}';''')
            return jsonify(data)
        except:
            return jsonify({'error': str(err)}), 500


if __name__ == '__main__':
    app.run(debug=False)
