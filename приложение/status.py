import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


def change_status(canvas):
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

    def open_edit_window(event, treeview, mas_label, table_name, mas_table,select):
        # Получаем идентификатор строки, на которую был выполнен двойной щелчок
        selected_item = treeview.selection()[0]
        # Получаем значения для выбранной строки
        values = treeview.item(selected_item, "values")
        print(table_name,mas_table)
        # Создаем новое окно для редактирования
        edit_window = tk.Toplevel(canvas)
        edit_window.title("Редактирование записи")
        edit_window.geometry("400x420")

        labels = mas_label
        entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, values[i])  # Заполняем поля текущими значениями
            if i == 0:
                entry['state'] = 'disabled'
            entries[label_text] = entry  # Сохраняем ссылки на поля ввода для дальнейшего использования

        # Функция для обновления записи в базе данных
        def save_changes():
            id_table = entries[labels[0]].get()

            quary=f"UPDATE `{table_name}` SET `{mas_table[1]}` = '{entries[labels[1]].get()}' WHERE `{mas_table[0]}` = '{id_table}';"

            print(quary)
            # Обновляем запись в базе данных
            conn = connect_to_db()
            cursor = conn.cursor()
            try:
                cursor.execute(quary)
                conn.commit()

                for row in treeview.get_children():
                    treeview.delete(row)

                data = load_data_from_db(select)
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

    label_employee = tk.Label(canvas, font=("Helvetica", 15), text='Сотрудники:')
    label_employee.place(x=50, y=50)
    treeview_employee = ttk.Treeview(canvas, columns=('#1', '#2'), show="headings")
    treeview_employee.heading('#1', text='Логин')
    treeview_employee.heading('#2', text='Статус')
    treeview_employee.place(x=50, y=80, height=400)
    z1='select логин, статус from сотрудник'
    data = load_data_from_db(z1)
    for item in data:
        treeview_employee.insert("", tk.END, values=item)
    treeview_employee.bind("<Double-1>", lambda e: open_edit_window(event=e, treeview=treeview_employee, mas_label=['логин', 'статус'],
                                                                    table_name='сотрудник', mas_table=['логин', 'статус'],
                                                                    select=z1))

    label_zakaz = tk.Label(canvas, font=("Helvetica", 15), text='Заказы:')
    label_zakaz.place(x=50, y=530)
    treeview_zakaz = ttk.Treeview(canvas, columns=('#1', '#2'), show="headings")
    treeview_zakaz.heading('#1', text='id_заказа')
    treeview_zakaz.heading('#2', text='Статус')
    treeview_zakaz.place(x=50, y=560, height=400)
    z2='select id_заказ, статус from заказ'
    data = load_data_from_db(z2)
    for item in data:
        treeview_zakaz.insert("", tk.END, values=item)
    treeview_zakaz.bind("<Double-1>", lambda e: open_edit_window(event=e, treeview=treeview_zakaz, mas_label=['id_заказ', 'статус'],
                                                                    table_name='заказ', mas_table=['id_заказ', 'статус'],
                                                                    select=z2))

    label_tovar = tk.Label(canvas, font=("Helvetica", 15), text='Товары:')
    label_tovar.place(x=530, y=50)
    treeview_tovar = ttk.Treeview(canvas, columns=('#1', '#2'), show="headings")
    treeview_tovar.heading('#1', text='id_товара')
    treeview_tovar.heading('#2', text='Статус')
    treeview_tovar.place(x=530, y=80, height=400)
    z3='select id_товара, статус from товар'
    data = load_data_from_db(z3)
    for item in data:
        treeview_tovar.insert("", tk.END, values=item)
    treeview_tovar.bind("<Double-1>",
                        lambda e: open_edit_window(event=e, treeview=treeview_tovar, mas_label=['id_товара', 'статус'],
                                                   table_name='товар', mas_table=['id_товара', 'статус'],
                                                   select=z3))

    label_tovar_zakaz = tk.Label(canvas, font=("Helvetica", 15), text='Товары в заказе:')
    label_tovar_zakaz.place(x=530, y=530)
    treeview_tovar_zakaz = ttk.Treeview(canvas, columns=('#1', '#2'), show="headings")
    treeview_tovar_zakaz.heading('#1', text='id_товара_в_заказе')
    treeview_tovar_zakaz.heading('#2', text='Статус')
    treeview_tovar_zakaz.place(x=530, y=560, height=400)
    z4='select id_товары_в_заказе, статус from `товары в заказе`'
    data = load_data_from_db(z4)
    for item in data:
        treeview_tovar_zakaz.insert("", tk.END, values=item)
    treeview_tovar_zakaz.bind("<Double-1>",
                        lambda e: open_edit_window(event=e, treeview=treeview_tovar_zakaz, mas_label=['id_товара_в заказе', 'статус'],
                                                   table_name='товары в заказе', mas_table=['id_товары_в_заказе', 'статус'],
                                                   select=z4))

    label_yacheyka = tk.Label(canvas, font=("Helvetica", 15), text='Ячейка:')
    label_yacheyka.place(x=1010, y=50)
    treeview_yacheyka = ttk.Treeview(canvas, columns=('#1', '#2'), show="headings")
    treeview_yacheyka.heading('#1', text='название')
    treeview_yacheyka.heading('#2', text='Статус')
    treeview_yacheyka.place(x=1010, y=80, height=400)
    z5='select наименование, статус from ячейка'
    data = load_data_from_db(z5)
    for item in data:
        treeview_yacheyka.insert("", tk.END, values=item)
    treeview_yacheyka.bind("<Double-1>",
                        lambda e: open_edit_window(event=e, treeview=treeview_yacheyka, mas_label=['название', 'статус'],
                                                   table_name='ячейка', mas_table=['наименование', 'статус'],
                                                   select=z5))

    label_kamera = tk.Label(canvas, font=("Helvetica", 15), text='Камера хранения:')
    label_kamera.place(x=1010, y=530)
    treeview_kamera = ttk.Treeview(canvas, columns=('#1', '#2'), show="headings")
    treeview_kamera.heading('#1', text='название')
    treeview_kamera.heading('#2', text='Статус')
    treeview_kamera.place(x=1010, y=560, height=400)
    z6='select название, статус from `камера_хранения_заказа`'
    data = load_data_from_db(z6)
    for item in data:
        treeview_kamera.insert("", tk.END, values=item)
    treeview_kamera.bind("<Double-1>",
                        lambda e: open_edit_window(event=e, treeview=treeview_kamera, mas_label=['название', 'статус'],
                                                   table_name='камера_хранения_заказа', mas_table=['название', 'статус'],
                                                   select=z6))

    label_information = tk.Label(canvas, font=("Helvetica", 15), text='Статусы:')
    label_information.place(x=1490, y=50)
    text_information = tk.Text(canvas, width=42, height=45, font=("Helvetica", 12))
    with open('статусы.txt', 'r', encoding="utf-8") as file:
        data = file.read()
        text_information.insert(tk.END, data)
    file.close()
    text_information['state'] = 'disabled'
    text_information.place(x=1490, y=100)


if __name__ == '__main__':
    # Основное окно
    root = tk.Tk()
    root.title("Управление заказами")
    # Canvas для отображения выбранного текста
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    change_status(canvas)
    root.mainloop()
