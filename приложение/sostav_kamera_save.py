import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def sostav_kamera(canvas):
    # Функция для выполнения запроса и заполнения второй таблицы
    def on_row_select(event):
        selected_item = tree_1.selection()[0]
        selected_id = tree_1.item(selected_item, 'values')[0]

        # Очистить вторую таблицу перед заполнением новыми данными
        for row in tree_2.get_children():
            tree_2.delete(row)

        # SQL запрос для получения данных по выбранной ячейке
        query = f"""
SELECT 
s1.id_товара,
z.наименование as "наименование товара",
z.`штрих-код`,
s1.марка,
s1.`qr-код`,
s2.статус as "статус товара", 
s3.id_заказ,
s3.статус as "статус заказа"
FROM `перечень товаров` z
JOIN товар s1 ON z.id_перечень_товаров = s1.`перечень товаров_id_перечень_товаров`
JOIN `товары в заказе` s2 ON s1.id_товара = s2.товар_id_товара
JOIN заказ s3 ON s2.заказ_id_заказ = s3.id_заказ
WHERE s3.камера_хранения_заказа_id_место_оформления_заказа = {selected_id} and s3.статус="готовится к отправке" or "проверяется";
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Заполняем вторую таблицу результатами запроса
        for row in result:
            tree_2.insert('', tk.END, values=row)

    # Функция для поиска по наименованию ячейки
    def search():
        search_term = entry_search.get()
        query = f"select * from камера_хранения_заказа where название LIKE '%{search_term}%'"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Очистить первую таблицу перед заполнением новыми данными
        for row in tree_1.get_children():
            tree_1.delete(row)

        # Заполняем первую таблицу результатами поиска
        for row in rows:
            tree_1.insert('', tk.END, values=row)

    # Создание первой таблицы для отображения данных из таблицы 'ячейка'
    tree_1 = ttk.Treeview(canvas, columns=('id_ячейки', 'наименование', 'статус'), show='headings')
    tree_1.heading('id_ячейки', text='ID Камера')
    tree_1.heading('наименование', text='Наименование')
    tree_1.heading('статус', text='Статус')
    tree_1.column('id_ячейки', width=100)
    tree_1.column('наименование', width=120)
    tree_1.column('статус', width=150)

    tree_1.place(x=50, y=150, height=750)

    fq=['#1', '#2', '#3', '#4', '#5', '#6',
        '#7',"#8"]
    # Создание таблицы для отображения результатов запроса
    tree_2 = ttk.Treeview(canvas, columns=(fq), show='headings')
    tree_2.heading('#1', text='ID Товара')
    tree_2.heading('#2', text='Наименование Товара')
    tree_2.heading('#3', text='Штрих-код')
    tree_2.heading('#4', text='Марка')
    tree_2.heading('#5', text='QR-код')
    tree_2.heading('#6', text='Статус товара')
    tree_2.heading('#7', text='id_заказа')
    tree_2.heading('#8', text='Статус заказа')
    for i in fq:
        tree_2.column(i, width=175)



    # Функция для копирования значения в буфер обмена
    def copy_to_clipboard(event):
        # Получаем координаты клика
        row_id = tree_2.identify_row(event.y)
        column_id = tree_2.identify_column(event.x)

        if row_id and column_id:
            # Получаем значение ячейки по клику
            cell_value = tree_2.set(row_id, column_id)
            if cell_value:
                messagebox.showinfo("Информирование", f"Скопировано: {cell_value}")
                canvas.clipboard_clear()
                canvas.clipboard_append(cell_value)

    tree_2.place(x=450, y=150, height=750)

    # Привязываем обработчик события клика по ячейке
    tree_2.bind("<Double-1>", copy_to_clipboard)

    # Поле для ввода текста для поиска
    entry_search = tk.Entry(canvas)
    entry_search.place(x=50, y=50, width=200)

    # Кнопка для выполнения поиска
    button_search = tk.Button(canvas, text="Поиск", command=search)
    button_search.place(x=270, y=47)

    # Загрузка данных для первой таблицы из базы данных
    cursor.execute("select * from камера_хранения_заказа")
    rows = cursor.fetchall()
    for row in rows:
        tree_1.insert('', tk.END, values=row)

    # Привязка функции к выбору строки в первой таблице
    tree_1.bind('<ButtonRelease-1>', on_row_select)


# Настройки подключения к базе данных
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sklad"
)

cursor = conn.cursor()
if __name__ == '__main__':
    # Создание основного окна
    root = tk.Tk()
    root.geometry('1920x1080')
    can = tk.Canvas(root, width=1920, height=1080)
    can.pack()
    # Запуск программы
    sostav_kamera(can)
    root.mainloop()
    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()
