import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import pyperclip


def zakaz_information(canvas):
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

    # Функция для обработки двойного клика по ячейке
    def on_double_click(event):
        row_id = treeview.identify_row(event.y)
        column_id = treeview.identify_column(event.x)

        # Получаем индекс столбца (например, '#1', '#2') и преобразуем его в число
        column_number = int(column_id.replace('#', ''))

        # Извлекаем значение ячейки
        cell_value = treeview.set(row_id, column_id)

        if column_number == 8:  # Столбец 10
            query = f"""
            SELECT * FROM сотрудник WHERE id_сотрудник IN 
            (SELECT сотрудник_id_сотрудник FROM менеджер WHERE id_менеджер = {cell_value})
            """
            load_employees(query)

        # Выполняем запросы в зависимости от столбца
        elif column_number == 10:  # Столбец 10
            query = f"""
            SELECT * FROM сотрудник WHERE id_сотрудник IN 
            (SELECT сотрудник_id_сотрудник FROM комплектовщик WHERE id_комплектовщик = {cell_value})
            """
            load_employees(query)
        elif column_number == 11:  # Столбец 11
            query = f"""
            SELECT * FROM сотрудник WHERE id_сотрудник IN 
            (SELECT сотрудник_id_сотрудник FROM `проверяющий комплектовку` WHERE id_проверяющий_комплектовку = {cell_value})
            """
            load_employees(query)

        elif column_number == 12:  # Столбец 12
            query = f"""
            SELECT * FROM сотрудник WHERE id_сотрудник IN 
            (SELECT сотрудник_id_сотрудник FROM `водитель` WHERE id_водитель = {cell_value})
            """
            load_employees(query)

    def button_click(button_name):
        # Очищаем текущее содержимое Treeview
        for row in worked_employee_treeview.get_children():
            worked_employee_treeview.delete(row)

        # Выполняем запрос к базе данных
        data = load_data_from_db(
            f'SELECT id_сотрудник, логин, фамилия, имя, отчество, специальность FROM сотрудник WHERE статус="в работе" and специальность="{button_name}";')

        # Заполняем Treeview новыми данными
        for row in data:
            worked_employee_treeview.insert('', tk.END, values=row)

        label.config(text=button_name)

    def copy_to_clipboard(event):
        # Получаем координаты клика
        row_id = worked_employee_treeview.identify_row(event.y)
        column_id = worked_employee_treeview.identify_column(event.x)

        if row_id and column_id:
            # Получаем значение ячейки по клику
            cell_value = worked_employee_treeview.set(row_id, column_id)
            if cell_value:
                messagebox.showinfo("Информирование", f"Скопировано: {cell_value}")
                pyperclip.copy(cell_value)

    def open_edit_window(event):
        # Получаем идентификатор строки, на которую был выполнен двойной щелчок
        selected_item = treeview.selection()[0]
        # Получаем значения для выбранной строки
        values = treeview.item(selected_item, "values")

        # Создаем новое окно для редактирования
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактирование записи")
        edit_window.geometry("400x420")

        # Метки и поля для ввода (id, логин, фамилия, имя, отчество, специальность)
        labels = [
            "id_заказ", "id_клиент", "время_на_сборку", "время_сборки", "время_проверки",
            "время_отправки", "статус", "логин менеджера",
            "логин комплектовщика",
            "логин проверяющего комплектовку",
            "логин водителя",
            "номер ячейки"
        ]
        entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, values[i])  # Заполняем поля текущими значениями
            entry['state'] = ['normal' if i in [8, 9, 10, 11] else 'disabled'][0]
            entries[label_text] = entry  # Сохраняем ссылки на поля ввода для дальнейшего использования

        # Функция для обновления записи в базе данных
        def save_changes():
            id_meneger = load_data_from_db(
                f'select id_менеджер from менеджер where сотрудник_id_сотрудник=(select id_сотрудник from сотрудник where логин="{entries["логин менеджера"].get()}" and статус="в работе");')[
                0][0]
            id_komplekt = load_data_from_db(
                f'select id_комплектовщик from комплектовщик where сотрудник_id_сотрудник=(select id_сотрудник from сотрудник where логин="{entries["логин комплектовщика"].get()}" and статус="в работе");')[
                0][0]
            id_prover = load_data_from_db(
                f'select id_проверяющий_комплектовку from `проверяющий комплектовку` where сотрудник_id_сотрудник=(select id_сотрудник from сотрудник where логин="{entries["логин проверяющего комплектовку"].get()}" and статус="в работе");')[
                0][0]
            id_voditel = load_data_from_db(
                f'select id_водитель from водитель where сотрудник_id_сотрудник=(select id_сотрудник from сотрудник where логин="{entries["логин водителя"].get()}" and статус="в работе");')[
                0][0]
            id_yacheyki = load_data_from_db(
                f'select id_место_оформления_заказа from камера_хранения_заказа where название="{entries["номер ячейки"].get()}" and статус!="заблокирована";')[
                0][0]
            quary = f'''
    UPDATE заказ
    SET 
        время_на_сборку = '{entries['время_на_сборку'].get()}','''
            for i in ["время_сборки", "время_проверки", "время_отправки", "статус"]:
                if entries[i].get() == 'None':
                    quary += f'''
        {i}=Null,'''
                else:
                    quary += f'''
        {i}='{entries[i].get()}','''

            quary += f'''
        клиент_id_клиент = {entries['id_клиент'].get()},   
        менеджер_id_менеджер = {id_meneger}, 
        камера_хранения_заказа_id_место_оформления_заказа = {id_yacheyki}, 
        `проверяющий комплектовку_id_проверяющий_комплектовку` = {id_prover}, 
        комплектовщик_id_комплектовщик = {id_komplekt},
        водитель_id_водитель = {id_voditel}
    WHERE id_заказ = {entries["id_заказ"].get()};
    '''
            print(quary)
            # Обновляем запись в базе данных
            conn = connect_to_db()
            cursor = conn.cursor()
            try:
                cursor.execute(quary)
                conn.commit()

                for row in treeview.get_children():
                    treeview.delete(row)

                data = load_data_from_db(big_request)
                for item in data:
                    treeview.insert("", tk.END, values=item)

                # Закрываем окно редактирования
                edit_window.destroy()
            except Exception as ex:
                messagebox.showerror("Ошибка", f"При выполнении запроса в БД возникла ошибка \n {ex}")

            conn.close()

        # Кнопка для сохранения изменений
        save_button = tk.Button(edit_window, text="Сохранить", command=save_changes)
        save_button.place(x=280, y=380)

    # Создаем таблицу Treeview с колонками из таблицы "заказ"
    columns = (
        "id_заказ", "id_клиент", "время_на_сборку", "время_сборки", "время_проверки",
        "время_отправки", "статус", "логин менеджера",
        "логин комплектовщика",
        "логин проверяющего комплектовку",
        "логин водителя",
        "номер ячейки"
    )

    treeview = ttk.Treeview(canvas, columns=columns, show="headings")

    # Устанавливаем заголовки для каждого столбца
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=150)
    big_request = '''
    SELECT 
        z.id_заказ,
        z.клиент_id_клиент as id_клиент,
        z.время_на_сборку,
        z.время_сборки,
        z.время_проверки,
        z.время_отправки,
        z.статус,
        s2.логин AS логин_менеджера,
        s1.логин AS логин_комплектовщика,
        s4.логин AS логин_проверяющего,
        s3.логин AS логин_водителя,
        s5.название as номер_ячейки
    FROM 
        заказ z
    -- Соединение с комплектовщиком
    JOIN 
        комплектовщик k ON z.`комплектовщик_id_комплектовщик` = k.id_комплектовщик
    JOIN 
        сотрудник s1 ON k.`сотрудник_id_сотрудник` = s1.id_сотрудник
    -- Соединение с менеджером
    JOIN 
        менеджер m ON z.`менеджер_id_менеджер` = m.id_менеджер
    JOIN 
        сотрудник s2 ON m.`сотрудник_id_сотрудник` = s2.id_сотрудник
    -- Соединение с водителем
    JOIN 
        водитель v ON z.`водитель_id_водитель` = v.id_водитель
    JOIN 
        сотрудник s3 ON v.`сотрудник_id_сотрудник` = s3.id_сотрудник
    -- Соединение с проверяющим
    JOIN 
        `проверяющий комплектовку` p ON z.`проверяющий комплектовку_id_проверяющий_комплектовку` = p.id_проверяющий_комплектовку
    JOIN 
        сотрудник s4 ON p.`сотрудник_id_сотрудник` = s4.id_сотрудник
    -- Соединение с ячейкой
    JOIN
        камера_хранения_заказа s5 ON z.камера_хранения_заказа_id_место_оформления_заказа = s5.id_место_оформления_заказа
    order by z.время_на_сборку desc;
    '''
    # Загружаем данные из базы данных
    data = load_data_from_db(big_request)

    # Заполняем таблицу данными из БД
    for item in data:
        treeview.insert("", tk.END, values=item)

    # Привязываем обработчик события двойного клика по ячейке
    treeview.bind("<Double-1>", on_double_click)

    treeview.place(x=50, y=550, height=400)

    worked_employee_treeview = ttk.Treeview(canvas, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show="headings")

    worked_employee_treeview.heading('#1', text='id_сотрудника')
    worked_employee_treeview.heading('#2', text='логин')
    worked_employee_treeview.heading('#3', text='фамилия')
    worked_employee_treeview.heading('#4', text='имя')
    worked_employee_treeview.heading('#5', text='отчество')
    worked_employee_treeview.heading('#6', text='специальность')

    worked_employee_treeview.place(x=500, y=80, height=400)

    # Привязываем обработчик события клика по ячейке
    worked_employee_treeview.bind("<Double-1>", copy_to_clipboard)
    treeview.bind("<Double-1>", open_edit_window)

    # Загружаем данные из базы данных
    data = load_data_from_db(
        'select id_сотрудник,логин,фамилия,имя,отчество,специальность from сотрудник where статус="в работе";')

    # Заполняем таблицу данными из БД
    for item in data:
        worked_employee_treeview.insert("", tk.END, values=item)

    # Создаем метку для отображения нажатой кнопки
    label = tk.Label(canvas, text="Специальность:", font=("Helvetica", 20))
    label.place(x=50, y=80)
    label = tk.Label(canvas, text="Специальность не выбрана", font=("Helvetica", 16))
    label.place(x=50, y=150)

    # Создаем кнопки
    buttons = [
        "Водитель",
        "Менеджер",
        "Комплектовщик",
        "Проверяющий комплектовку"
    ]

    for index, button_name in enumerate(buttons):
        button = tk.Button(canvas, font=("Helvetica", 12), text=button_name,
                           command=lambda name=button_name: button_click(name))
        button.place(x=50, y=200 + index * 40, width=300)


if __name__ == '__main__':
    # Создание основного окна
    root = tk.Tk()
    root.geometry('1920x1080')
    can = tk.Canvas(root, width=1920, height=1080)
    can.pack()
    # Запуск программы
    zakaz_information(can)
    root.mainloop()
    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()
