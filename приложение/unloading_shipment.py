import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import pyperclip


def postavka_information(canvas):
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

    def copy_to_clipboard2(event):
        # Получаем координаты клика
        row_id = treeview_tovar.identify_row(event.y)
        column_id = treeview_tovar.identify_column(event.x)

        if row_id and column_id:
            # Получаем значение ячейки по клику
            cell_value = treeview_tovar.set(row_id, column_id)
            if cell_value:
                messagebox.showinfo("Информирование", f"Скопировано: {cell_value}")
                pyperclip.copy(cell_value)

    def open_edit_window(event):
        # Получаем идентификатор строки, на которую был выполнен двойной щелчок
        selected_item = treeview.selection()[0]
        # Получаем значения для выбранной строки
        values = treeview.item(selected_item, "values")

        # Создаем новое окно для редактирования
        edit_window = tk.Toplevel(canvas)
        edit_window.title("Редактирование записи")
        edit_window.geometry("400x420")

        # Метки и поля для ввода (id, логин, фамилия, имя, отчество, специальность)
        labels = [
            "id_поставки", "дата отгрузки", "дата приёма", "логин менеджера", "логин принимающего поставку",
            "логин водителя"
        ]
        entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, values[i])  # Заполняем поля текущими значениями
            entry['state'] = ['normal' if i in [4, 5] else 'disabled'][0]
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

    def find_tovar_from_postavka(event):
        first_value = treeview.item(treeview.selection()[0])['values'][0]
        quar = f'''
select 
z.`id_товара`,
s4.наименование,
s4.`штрих-код`,
z.`марка`,
z.`qr-код`,
z.`срок_годности`,
z.`время_распределения`,
s3.наименование as "имя ячейки",
s1.логин as "логин комплектовщика ячеек",
s2.логин as "логин менеджера",
z.`статус`
 from товар z

-- соединение с комплектовщик ячеек
JOIN 
    `комплектовщик ячеек` k ON z.`комплектовщик ячеек_id_комплектовщик_ячеек` = k.`id_комплектовщик_ячеек`
JOIN 
    сотрудник s1 ON k.`сотрудник_id_сотрудник` = s1.id_сотрудник
-- Соединение с менеджером
JOIN 
    менеджер m ON z.`менеджер_id_менеджер` = m.id_менеджер
JOIN 
    сотрудник s2 ON m.`сотрудник_id_сотрудник` = s2.id_сотрудник
-- Соединение с ячейкой
JOIN
	ячейка s3 ON z.ячейка_id_ячейки = s3.id_ячейки
-- соединение с перечнем товаров
JOIN
	`перечень товаров` s4 ON z.`перечень товаров_id_перечень_товаров` = s4.id_перечень_товаров
    
 where поставка_id_поставка={first_value}
 order by время_распределения desc;        
        '''
        dates = load_data_from_db(quar)
        for row in treeview_tovar.get_children():
            treeview_tovar.delete(row)

        for row in dates:
            treeview_tovar.insert('', tk.END, values=row)
        label_postavka['text']=f"Поставка: {first_value}"
    # Создаем таблицу Treeview с колонками из таблицы "заказ"
    columns = (
        "id_поставки", "дата отгрузки", "дата приёма", "логин менеджера", "логин принимающего поставку",
        "логин водителя"
    )

    treeview = ttk.Treeview(canvas, columns=columns, show="headings")

    # Устанавливаем заголовки для каждого столбца
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100)
    big_request = '''
select 
z.id_поставка,
z.`дата отгрузки`, 
z.`дата приёма`,
s2.логин as "логин менеджера",
s1.логин as "логин принимающего поставку",
s3.логин as "логин водителя"
from поставка z
-- соединение с принимающим поставку
JOIN 
    `принимающий поставку` k ON z.`принимающий поставку_id_принимающий_поставку` = k.`id_принимающий_поставку`
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
order by z.`дата отгрузки` desc;
    '''
    # Загружаем данные из базы данных
    data = load_data_from_db(big_request)

    # Заполняем таблицу данными из БД
    for item in data:
        treeview.insert("", tk.END, values=item)

    treeview.place(x=30, y=550, height=400)

    # Загружаем данные из базы данных
    data = load_data_from_db(
        'select id_сотрудник,логин,фамилия,имя,отчество,специальность from сотрудник where статус="в работе";')

    worked_employee_treeview = ttk.Treeview(canvas, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show="headings")
    # Заполняем таблицу данными из БД
    for item in data:
        worked_employee_treeview.insert("", tk.END, values=item)
    worked_employee_treeview.heading('#1', text='id_сотрудника')
    worked_employee_treeview.heading('#2', text='логин')
    worked_employee_treeview.heading('#3', text='фамилия')
    worked_employee_treeview.heading('#4', text='имя')
    worked_employee_treeview.heading('#5', text='отчество')
    worked_employee_treeview.heading('#6', text='специальность')
    worked_employee_treeview.place(x=500, y=80, height=400)

    # Создаем метку для отображения нажатой кнопки
    label = tk.Label(canvas, text="Специальность:", font=("Helvetica", 20))
    label.place(x=50, y=80)
    label = tk.Label(canvas, text="Специальность не выбрана", font=("Helvetica", 16))
    label.place(x=50, y=150)

    # Создаем кнопки
    buttons = [
        "Водитель",
        "Менеджер",
        "Комплектовщик ячеек",
        "Принимающий поставку"
    ]

    for index, button_name in enumerate(buttons):
        button = tk.Button(canvas, font=("Helvetica", 12), text=button_name,
                           command=lambda name=button_name: button_click(name))
        button.place(x=50, y=200 + index * 40, width=300)

    label_postavka = tk.Label(canvas, text="Поставка: ?", font=("Helvetica", 20))
    label_postavka.place(x=700, y=500)

    df=['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11']
    treeview_tovar = ttk.Treeview(canvas, columns=(df
    ), show="headings")

    treeview_tovar.heading('#1', text='id_товара')
    treeview_tovar.heading('#2', text='наименование')
    treeview_tovar.heading('#3', text='штрих-код')
    treeview_tovar.heading('#4', text='марка')
    treeview_tovar.heading('#5', text='qr-код')
    treeview_tovar.heading('#6', text='срок годности')
    treeview_tovar.heading('#7', text='время распределения')
    treeview_tovar.heading('#8', text='имя ячейки')
    treeview_tovar.heading('#9', text='логин комплектовщка ячеек')
    treeview_tovar.heading('#10', text='логин менеджера')
    treeview_tovar.heading('#11', text='статус')

    for i in df:
        treeview_tovar.column(i,width=110)

    treeview_tovar.place(x=650, y=550, height=400)

    # Привязываем обработчик события клика по ячейке
    worked_employee_treeview.bind("<Double-1>", copy_to_clipboard)
    treeview.bind("<<TreeviewSelect>>", find_tovar_from_postavka)
    treeview.bind("<Double-1>", open_edit_window)
    treeview_tovar.bind("<Double-1>", copy_to_clipboard2)

if __name__ == '__main__':
    # Создание основного окна
    root = tk.Tk()
    root.geometry('1920x1080')
    can = tk.Canvas(root, width=1920, height=1080)
    can.pack()
    # Запуск программы
    postavka_information(can)
    root.mainloop()
    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()
