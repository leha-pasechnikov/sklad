import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox


def hand_mode(canvas, id_meneger):
    connection = None
    tree = None
    current_table = None

    # Соединение с БД
    def connect_to_db():
        nonlocal connection
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='sklad',
                user='root',
                password=''
            )
            if connection.is_connected():
                load_table_list()
        except Error as e:
            messagebox.showerror("Ошибка подключения", f"Ошибка: {e}")

    # Загрузка списка таблиц
    def load_table_list():
        nonlocal current_table
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        table_dropdown['values'] = table_names
        if table_names:
            table_dropdown.current(0)
            load_table(None)

    # Загрузка таблицы
    def load_table(event):
        nonlocal tree, current_table
        current_table = table_dropdown.get()
        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE `{current_table}`")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]

        if tree:
            tree.destroy()

        tree = ttk.Treeview(canvas, columns=column_names, show='headings')
        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.place(x=50, y=100, width=1820, height=800)

        cursor.execute(f"SELECT * FROM `{current_table}`")
        records = cursor.fetchall()
        for row in records:
            tree.insert('', tk.END, values=row)

        tree.bind("<Double-1>", on_row_double_click)

    # Двойной клик для редактирования строки
    def on_row_double_click(event):
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        open_edit_window(values)

    # Добавление записи
    def add_record():
        open_edit_window(None)

    # Редактирование записи
    def edit_record():
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0], 'values')
            open_edit_window(values)
        else:
            messagebox.showwarning("Выбор строки", "Пожалуйста, выберите строку для редактирования.")

    # Удаление записи
    def delete_record():
        selected_item = tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить эту запись?")
            if confirm:
                values = tree.item(selected_item[0], 'values')
                cursor = connection.cursor()
                query = f"DELETE FROM `{current_table}` WHERE `{tree['columns'][0]}` = {values[0]};"
                try:
                    cursor.execute(query)
                    connection.commit()
                    tree.delete(selected_item[0])
                    messagebox.showinfo("Удаление", "Запись успешно удалена.")
                except Exception as ex:
                    messagebox.showerror("Ошибка удаления", ex)
        else:
            messagebox.showwarning("Выбор строки", "Пожалуйста, выберите строку для удаления.")

    # Открытие окна для редактирования/добавления записи
    def open_edit_window(values):
        if level>=2:
            edit_window = tk.Toplevel(canvas)
            edit_window.title("Редактирование записи")
            cursor = connection.cursor()
            cursor.execute(f"DESCRIBE `{current_table}`")
            columns = cursor.fetchall()

            entries = {}
            for i, col in enumerate(columns):
                col_name = col[0]
                label = tk.Label(edit_window, text=col_name)
                label.grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=5, pady=5)
                if values:
                    entry.insert(0, values[i])
                entries[col_name] = entry

        # Сохранение записи
        def save_record():
            data = {col: entries[col].get() for col in entries}
            cursor = connection.cursor()
            if values:
                try:
                    columns_str = ''
                    for key in data:
                        if data[key] != 'None':
                            columns_str += f'`{key}`= "{data[key]}",'
                        else:
                            columns_str += f'`{key}`= Null,'
                    columns_str = columns_str[:-1]
                    query = f"UPDATE `{current_table}` SET {columns_str} WHERE `{tree['columns'][0]}` = {values[0]};"
                    cursor.execute(query)

                except Exception as ex:
                    messagebox.showerror("Ошибка редактирования", ex)
            else:
                columns_str = ', '.join(data.keys())
                values_str = ', '.join(f'"{data[key]}"' if data[key] != 'None' else 'Null' for key in data)
                try:
                    query = f"INSERT INTO `{current_table}` ({columns_str}) VALUES ({values_str})"
                    cursor.execute(query)
                except Exception as ex:
                    messagebox.showerror("Ошибка добавления", ex)

            connection.commit()
            load_table(None)
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить", command=save_record)
        save_button.grid(row=len(columns), column=0, columnspan=2, padx=5, pady=5)

    # Выпадающий список таблиц
    table_dropdown = ttk.Combobox(canvas, state="readonly", font=("Arial", 12))
    table_dropdown.place(x=80, y=50)
    table_dropdown.bind("<<ComboboxSelected>>", load_table)



    # Кнопки для управления записями
    add_button = tk.Button(canvas, text="Добавить запись", command=add_record, font=("Arial", 15))
    add_button.place(x=100, y=930)

    edit_button = tk.Button(canvas, text="Редактировать запись", command=edit_record, font=("Arial", 15))
    edit_button.place(x=300, y=930)

    delete_button = tk.Button(canvas, text="Удалить запись", command=delete_record, font=("Arial", 15))
    delete_button.place(x=550, y=930)

    conn = mysql.connector.connect(
        host="localhost",  # Замените на ваш хост
        user="root",  # Замените на ваше имя пользователя
        password="",  # Замените на ваш пароль
        database="sklad"  # Название базы данных
    )
    cursor = conn.cursor()
    cursor.execute(f'select уровень_доступа from сотрудник where id_сотрудник={id_meneger}')
    level = cursor.fetchall()[0][0]
    conn.close()
    if level<=1:
        delete_button['state']='disabled'
        edit_button['state'] = 'disabled'

    connect_to_db()


if __name__ == '__main__':
    # Создание основного окна
    root = tk.Tk()
    root.geometry('1920x1080')
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    # Запуск программы
    hand_mode(canvas,31)
    root.mainloop()
