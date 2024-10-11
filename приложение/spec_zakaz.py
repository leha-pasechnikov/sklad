import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import messagebox


def spec_zakaz(canvas, id_meneger):
    global STAGE, zakaz_inform

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

    def toggle_entry():
        mas = ["время_на_сборку",
               "логин комплектовщика",
               "логин проверяющего комплектовку",
               "логин водителя",
               "название ячейки"]
        if var.get() == 1:
            for i in mas:
                entries[i]['state'] = 'normal'
                entries[i].delete(0, 'end')
            notebook.tab(0, state='normal')
            notebook.select(0)
        else:
            for i in mas:
                entries[i].delete(0, 'end')
                entries[i].insert(0, 'автоматическое')
                entries[i]['state'] = 'disabled'
            notebook.select(1)
            notebook.tab(0, state='disabled')

    def add_new_zakaz(entr):
        print(entr)
        values = []
        for row in treeview_zakaz_product.get_children():
            values.append(treeview_zakaz_product.item(row, 'values'))
        print(values)
        print('выполнить запрос')

    def create_order_tab(notebook):
        def copy_to_clipboard(event):
            # Получаем координаты клика
            row_id = worked_employee_treeview.identify_row(event.y)
            column_id = worked_employee_treeview.identify_column(event.x)

            if row_id and column_id:
                # Получаем значение ячейки по клику
                cell_value = worked_employee_treeview.set(row_id, column_id)
                if cell_value:
                    messagebox.showinfo("Информирование", f"Скопировано: {cell_value}")
                    canvas.clipboard_append(cell_value)

        def copy_to_clipboard1(event):
            # Получаем координаты клика
            row_id = camera_treeview.identify_row(event.y)
            column_id = camera_treeview.identify_column(event.x)

            if row_id and column_id:
                # Получаем значение ячейки по клику
                cell_value = camera_treeview.set(row_id, column_id)
                if cell_value:
                    messagebox.showinfo("Информирование", f"Скопировано: {cell_value}")
                    canvas.clipboard_append(cell_value)

        # Функция для поиска по наименованию ячейки
        def search():
            rows = load_data_from_db(
                f"SELECT * FROM камера_хранения_заказа WHERE название LIKE '%{entry_search.get()}%'")

            # Очистить первую таблицу перед заполнением новыми данными
            for row in camera_treeview.get_children():
                camera_treeview.delete(row)

            # Заполняем первую таблицу результатами поиска
            for row in rows:
                camera_treeview.insert('', tk.END, values=row)

        def do_id_client(id):
            entry_id_client.delete(0, 'end')
            entry_id_client.insert(0,
                                   str(load_data_from_db(
                                       f'SELECT клиент_id_клиент from заказ where id_заказ = {id}')[0][
                                           0]))
            entry_id_client.focus_set()

        """Создает вкладку 'Заказ'."""
        order_frame = tk.Frame(notebook, bg='#dcdcde', width=1330, height=700)
        notebook.add(order_frame, text='Заказ')

        # Загружаем данные из базы данных
        data = load_data_from_db(
            'select id_сотрудник,логин,фамилия,имя,отчество,специальность from сотрудник where статус="в работе";')

        worked_employee_treeview = ttk.Treeview(order_frame, columns=('#1', '#2', '#3', '#4', '#5', '#6'),
                                                show="headings")
        # Заполняем таблицу данными из БД
        for item in data:
            worked_employee_treeview.insert("", tk.END, values=item)
        worked_employee_treeview.heading('#1', text='id_сотрудника')
        worked_employee_treeview.heading('#2', text='логин')
        worked_employee_treeview.heading('#3', text='фамилия')
        worked_employee_treeview.heading('#4', text='имя')
        worked_employee_treeview.heading('#5', text='отчество')
        worked_employee_treeview.heading('#6', text='специальность')
        worked_employee_treeview.place(x=20, y=20, height=400)

        label = tk.Label(order_frame, text="Введите id заказа, который нужно дособрать")
        label.place(x=20, y=450)
        entry_id_zakaz = tk.Entry(order_frame, width=40)
        entry_id_zakaz.place(x=20, y=500)
        give_id = tk.Button(order_frame, text="Получить id_клиент",
                            command=lambda: do_id_client(entry_id_zakaz.get()))
        give_id.place(x=20, y=550)
        entry_id_client = tk.Entry(order_frame, width=40)
        entry_id_client.place(x=20, y=600)

        # Кнопка для выполнения поиска
        button_search = tk.Button(order_frame, text="Поиск", command=search)
        button_search.place(x=810, y=450)
        # Поле для ввода текста для поиска
        entry_search = tk.Entry(order_frame)
        entry_search.place(x=600, y=450, width=200)

        camera_data = load_data_from_db('select * from камера_хранения_заказа')
        camera_treeview = ttk.Treeview(order_frame, columns=('#1', '#2', '#3'), show="headings")
        # Заполняем таблицу данными из БД
        for item in camera_data:
            camera_treeview.insert("", tk.END, values=item)
        camera_treeview.heading('#1', text='id')
        camera_treeview.heading('#2', text='название')
        camera_treeview.heading('#3', text='статус')
        camera_treeview.place(x=600, y=480, height=200)

        worked_employee_treeview.bind("<Double-1>", copy_to_clipboard)
        camera_treeview.bind("<Double-1>", copy_to_clipboard1)

    def create_product_tab(notebook):
        def search_product():
            rows = load_data_from_db(
                f"SELECT * FROM `перечень товаров` WHERE `штрих-код` LIKE '%{entry_search_product.get()}%'")

            # Очистить первую таблицу перед заполнением новыми данными
            for row in treeview_all.get_children():
                treeview_all.delete(row)

            # Заполняем первую таблицу результатами поиска
            for row in rows:
                treeview_all.insert('', tk.END, values=row)

        def do_treeview_all_product():
            selected_item = treeview_all.selection()[0]
            selected_id = treeview_all.item(selected_item, 'values')[0]
            for row in treeview_all_product.get_children():
                treeview_all_product.delete(row)
            treeview_all_product_data = load_data_from_db(
                f'select id_товара from товар where (`перечень товаров_id_перечень_товаров` = {selected_id} and статус="свободен" and (срок_годности > current_date or срок_годности is null)) order by время_распределения;')
            for item in treeview_all_product_data:
                treeview_all_product.insert("", tk.END, values=item)

        def add_tovar_zakaz(event):
            # Показываем messagebox с вопросом
            result = messagebox.askyesno("Подтверждение", "Добавить это значение?")
            if result:
                selected_item = treeview_all_product.selection()[0]
                selected_id = treeview_all_product.item(selected_item, 'values')
                values = []
                for row in treeview_zakaz_product.get_children():
                    values.append(treeview_zakaz_product.item(row, 'values'))
                if selected_id in values:
                    messagebox.showerror("Ошибка", "Этот товар уже есть в списке")
                else:
                    treeview_zakaz_product.insert("", tk.END, values=(selected_id))  # Пример: вставляем значение 1

        def on_double_click(event):
            # Получаем выделенную строку
            selected_item = treeview_zakaz_product.focus()

            if selected_item:
                # Получаем данные из выделенной строки (ячейки)
                cell_value = treeview_zakaz_product.item(selected_item, "values")

                # Всплывающее окно с подтверждением удаления
                response = messagebox.askyesno("Подтверждение удаления",
                                               f"Вы действительно хотите удалить выделенный товар: {cell_value[0]}?")

                if response:  # Если пользователь подтвердил удаление
                    treeview_zakaz_product.delete(selected_item)

        """Создает вкладку 'Товар'."""
        product_frame = tk.Frame(notebook, bg='#dcdcde')
        notebook.add(product_frame, text='Товар')

        # Кнопка для выполнения поиска
        button_search_product = tk.Button(product_frame, text="Поиск", command=search_product)
        button_search_product.place(x=270, y=20)
        # Поле для ввода текста для поиска
        entry_search_product = tk.Entry(product_frame)
        entry_search_product.place(x=50, y=20, width=200)

        treeview_all_data = load_data_from_db('select * from `перечень товаров`')
        treeview_all = ttk.Treeview(product_frame, columns=('#1', '#2', '#3'), show="headings")
        # Заполняем таблицу данными из БД
        for item in treeview_all_data:
            treeview_all.insert("", tk.END, values=item)
        treeview_all.heading('#1', text='id')
        treeview_all.heading('#2', text='название')
        treeview_all.heading('#3', text='штрих-код')
        treeview_all.place(x=50, y=50, height=600)

        treeview_all_product = ttk.Treeview(product_frame, columns=('#1'), show="headings")
        treeview_all_product.heading('#1', text='id товара')
        treeview_all_product.place(x=750, y=50, height=600)

        treeview_zakaz_product = ttk.Treeview(product_frame, columns=('#1'), show="headings")
        treeview_zakaz_product.heading('#1', text='id товаров в заказе')
        treeview_zakaz_product.place(x=1050, y=50, height=600)

        treeview_all.bind("<Double-1>", lambda event: do_treeview_all_product())
        treeview_all_product.bind("<Double-1>", add_tovar_zakaz)
        treeview_zakaz_product .bind("<Double-1>", on_double_click)

        tk.Label(product_frame, text=">", font=("Arial", 32), bg='#dcdcde').place(x=690, y=310)
        tk.Label(product_frame, text=">", font=("Arial", 32), bg='#dcdcde').place(x=980, y=310)

    # Метки и поля для ввода (id, логин, фамилия, имя, отчество, специальность)
    labels = [
        "id_заказ", "id_клиент", "время_на_сборку", "время_сборки", "время_проверки",
        "время_отправки", "статус", "логин менеджера",
        "логин комплектовщика",
        "логин проверяющего комплектовку",
        "логин водителя",
        "название ячейки"
    ]
    entries = {}

    # Определим отступ для рамки вокруг элементов
    padding = 20
    # Определим координаты для размещения элементов
    x_start = 100
    y_start = 100
    y_spacing = 60

    # Найдем максимальные размеры элементов для рамки
    max_width = 0
    max_height = y_start + y_spacing * len(labels) + 40  # Общая высота

    for i, label_text in enumerate(labels):
        label = tk.Label(canvas, text=label_text)
        label.place(x=x_start, y=y_start + y_spacing * i)
        if label_text == "время_на_сборку":
            tk.Label(canvas, text='ГГГГ-ММ-ДД ЧЧ:ММ:СС').place(x=x_start, y=y_start + y_spacing * i + 20)

        entry = tk.Entry(canvas)
        entry.place(x=x_start + 220, y=y_start + y_spacing * i)

        # Сохраняем ссылки на поля ввода для дальнейшего использования
        entries[label_text] = entry
        # Определяем максимальную ширину для рамки

        max_width = max(max_width, x_start + 150 + 200)

    entries["id_заказ"].insert(0, 'автоматическое')
    entries["id_заказ"]['state'] = 'disabled'
    entries["статус"].insert(0, 'собирается')
    entries["статус"]['state'] = 'disabled'
    entries["время_сборки"].insert(0, 'None')
    entries["время_сборки"]['state'] = 'disabled'
    entries["время_проверки"].insert(0, 'None')
    entries["время_проверки"]['state'] = 'disabled'
    entries["время_отправки"].insert(0, 'None')
    entries["время_отправки"]['state'] = 'disabled'
    entries["логин менеджера"].insert(0,
                                      load_data_from_db(f"select логин from сотрудник where id_сотрудник={id_meneger}")[
                                          0][0])
    entries["логин менеджера"]['state'] = 'disabled'
    # Обновляем максимальную ширину с учетом кнопки
    max_width = max(max_width, x_start + 150 + 150)

    # Создание прямоугольника с отступами
    canvas.create_rectangle(
        x_start - padding,
        y_start - padding,
        max_width + padding,
        max_height + padding,
        outline="black", width=2
    )

    var = tk.IntVar(value=1)  # Переменная для хранения состояния Radiobutton
    # Радиокнопки
    rb1 = tk.Radiobutton(canvas, font=("Helvetica", 15), text="Ручная настройка", variable=var, value=1,
                         command=toggle_entry)
    rb2 = tk.Radiobutton(canvas, font=("Helvetica", 15), text="Автоматическая настройка", variable=var, value=2,
                         command=toggle_entry)
    rb1.place(x=500, y=850)
    rb2.place(x=500, y=800)

    # Создаем Notebook
    notebook = ttk.Notebook(canvas)
    notebook.place(x=500, y=50)

    # Создаем вкладки
    create_order_tab(notebook)
    create_product_tab(notebook)

    button_add_zakaz = tk.Button(canvas, font=("Helvetica", 15), text="Создать заказ",
                                 command=lambda: add_new_zakaz([entries[i].get() for i in entries]))
    button_add_zakaz.place(x=1600, y=850)
    notebook.select(1)


STAGE = 0
zakaz_inform = []
if __name__ == '__main__':
    # Основное окно

    root = tk.Tk()
    root.title("Управление заказами")
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()

    spec_zakaz(canvas, 18)
    root.mainloop()
