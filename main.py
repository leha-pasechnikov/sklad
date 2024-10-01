import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактирование и удаление данных из MySQL")
        self.connection = None
        self.tree = None
        self.current_table = None

        # Фреймы для интерфейса
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.X)

        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)

        # Выпадающий список таблиц
        self.table_dropdown = ttk.Combobox(self.table_frame, state="readonly")
        self.table_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table)

        # Кнопки для добавления, редактирования и удаления
        self.add_button = tk.Button(self.button_frame, text="Добавить запись", command=self.add_record)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(self.button_frame, text="Редактировать запись", command=self.edit_record)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Удалить запись", command=self.delete_record)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Соединение с БД
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='sklad',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                self.load_table_list()
        except Error as e:
            messagebox.showerror("Ошибка подключения", f"Ошибка: {e}")

    def load_table_list(self):
        """Загружаем список таблиц и добавляем их в выпадающий список"""
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        self.table_dropdown['values'] = table_names
        if table_names:
            self.table_dropdown.current(0)
            self.load_table(None)

    def load_table(self, event):
        """Загружаем данные и структуру выбранной таблицы"""
        self.current_table = self.table_dropdown.get()
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE `{self.current_table}`")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]

        if self.tree:
            self.tree.destroy()

        self.tree = ttk.Treeview(self.tree_frame, columns=column_names, show='headings')
        for col in column_names:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        cursor.execute(f"SELECT * FROM `{self.current_table}`")
        records = cursor.fetchall()
        for row in records:
            self.tree.insert('', tk.END, values=row)

        self.tree.bind("<Double-1>", self.on_row_double_click)

    def on_row_double_click(self, event):
        """Обработка двойного клика на строке для редактирования записи"""
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        self.open_edit_window(values)

    def add_record(self):
        """Открываем окно для добавления новой записи"""
        self.open_edit_window(None)

    def edit_record(self):
        """Редактирование выбранной строки"""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], 'values')
            self.open_edit_window(values)
        else:
            messagebox.showwarning("Выбор строки", "Пожалуйста, выберите строку для редактирования.")

    def delete_record(self):
        """Удаление выбранной строки"""
        selected_item = self.tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить эту запись?")
            if confirm:
                values = self.tree.item(selected_item[0], 'values')
                cursor = self.connection.cursor()
                query = f"DELETE FROM `{self.current_table}` WHERE `{self.tree['columns'][0]}` = {values[0]};"
                try:
                    cursor.execute(query)
                    self.connection.commit()
                    self.tree.delete(selected_item[0])
                    messagebox.showinfo("Удаление", "Запись успешно удалена.")
                except Exception as ex:
                    messagebox.showerror("Ошибка удаления", ex)
        else:
            messagebox.showwarning("Выбор строки", "Пожалуйста, выберите строку для удаления.")

    def open_edit_window(self, values):
        """Открываем окно для редактирования или добавления записи"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование записи")
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE `{self.current_table}`")
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

        def save_record():
            data = {col: entries[col].get() for col in entries}
            cursor = self.connection.cursor()
            if values:
                # Редактирование существующей записи
                try:
                    columns_str=''
                    for keys in data:
                        if data[keys] != 'None':
                            columns_str+=f'`{keys}`= "{data[keys]}",'
                        else:
                            columns_str += f'`{keys}`= Null,'
                    columns_str=columns_str[:-1]
                    query = f"UPDATE `{self.current_table}` SET {columns_str} WHERE `{self.tree['columns'][0]}` = {values[0]};"
                    cursor.execute(query)

                except Exception as ex:
                    messagebox.showerror("Ошибка редактирования", ex)
            else:
                # Добавление новой записи
                columns_str = ', '.join(data.keys())
                values_str=''
                for i in data:
                    if data[i] != "None":
                        values_str+=f'"{data[i]}",'
                    else:
                        values_str += 'Null,'
                values_str=values_str[:-1]
                try:
                    query = f"INSERT INTO `{self.current_table}` ({columns_str}) VALUES ({values_str})"
                    cursor.execute(query)
                except Exception as ex:
                    messagebox.showerror("Ошибка добавления", ex)

            self.connection.commit()
            self.load_table(None)
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить", command=save_record)
        save_button.grid(row=len(columns), column=0, columnspan=2, padx=5, pady=5)


# Создание основного окна
root = tk.Tk()
app = DatabaseApp(root)
root.mainloop()
