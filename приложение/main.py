import tkinter as tk
from tkinter import messagebox
from work_shedule import work_shedule
from hand_mode import hand_mode
from barcode_mode import barcode_mode


# Функция для обработки нажатия на пункты меню
def update_label(text):
    global status_variable
    status_variable.set(text)


# Основное окно
root = tk.Tk()
root.title("Управление заказами")

# Переменная для хранения статуса выбранного пункта меню
status_variable = tk.StringVar()
status_variable.set("Выберите пункт меню")

# Canvas для отображения выбранного текста
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()

# Метка на Canvas
label = tk.Label(root, textvariable=status_variable, font=("Arial", 16))
canvas.create_window(1000, 50, window=label)


# Функция для выхода
def exit_app():
    if messagebox.askokcancel("Выйти", "Вы действительно хотите выйти?"):
        root.quit()


# Создание меню
menu_bar = tk.Menu(root)

# Меню "Файл"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Выйти", command=exit_app)
menu_bar.add_cascade(label="Файл", menu=file_menu)


# # Функция для отображения графика работы
# def work_shedule(can: tk.Canvas):
#     # Очистка canvas
#     for widget in can.winfo_children():
#         widget.destroy()
#
#     # Добавляем кнопки на canvas
#     add_button = tk.Button(can, text="Добавить запись", command=lambda: print('1'))
#     add_button.place(x=5, y=50)
#
#     edit_button = tk.Button(can, text="Редактировать запись", command=lambda: print('2'))
#     edit_button.place(x=5, y=100)


# Функция для отображения успеваемости сотрудников (очистка Canvas)
def switch(comanda: str):
    # Очистка canvas
    for widget in canvas.winfo_children():
        widget.destroy()
    try:
        eval(comanda)
    except:
        print('переход невозможен')


# Меню "Режим"
mode_menu = tk.Menu(menu_bar, tearoff=0)
mode_menu.add_command(label="Ручной", command=lambda: switch('hand_mode(canvas)'))
menu_bar.add_cascade(label="Режим", menu=mode_menu)

# Меню "Сотрудники"
employees_menu = tk.Menu(menu_bar, tearoff=0)
employees_menu.add_command(label="График работы", command=lambda: switch('work_shedule(canvas)'))
employees_menu.add_command(label="Успеваемость", command=lambda: switch('update_label("Успеваемость")'))
employees_menu.add_command(label="Статистика", command=lambda: update_label("Сотрудники: Статистика"))
menu_bar.add_cascade(label="Сотрудники", menu=employees_menu)

# Меню "Ячейки"
cells_menu = tk.Menu(menu_bar, tearoff=0)
cells_menu.add_command(label="Состав", command=lambda: update_label("Ячейки: Состав"))
menu_bar.add_cascade(label="Ячейки", menu=cells_menu)

# Меню "Заказы"
orders_menu = tk.Menu(menu_bar, tearoff=0)
orders_menu.add_command(label="Информация", command=lambda: update_label("Заказы: Информация"))
orders_menu.add_command(label="Специальные заказы", command=lambda: update_label("Заказы: Специальные заказы"))
menu_bar.add_cascade(label="Заказы", menu=orders_menu)

# Меню "Штрих-код"
barcode_menu = tk.Menu(menu_bar, tearoff=0)
barcode_menu.add_command(label="Распечатать", command=lambda: switch('barcode_mode(canvas)'))
menu_bar.add_cascade(label="Штрих-код", menu=barcode_menu)

# Устанавливаем меню в главное окно
root.config(menu=menu_bar)

# Запуск главного цикла
root.mainloop()
