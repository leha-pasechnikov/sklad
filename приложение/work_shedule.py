import tkinter as tk
import calendar
from datetime import datetime, timedelta


def work_shedule(canvas):
    # Функция для обновления меток с датами
    def update_label():
        start_date = datetime(current_date.year, current_date.month, 1)  # Начало месяца
        _, last_day = calendar.monthrange(current_date.year, current_date.month)
        end_date = datetime(current_date.year, current_date.month, last_day)  # Конец месяца

        # Обновляем текст метки
        month_label.config(text=f"({months_ru[current_date.month - 1]} {current_date.year})")
        range_label.config(text=f"({start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')})")
        day_count = 1
        for row in range(ROWS):
            if row < current_date.replace(day=1).weekday():
                buttons[row][0].config(text='', state='disabled')
            else:
                buttons[row][0].config(text=str(day_count), state='normal')
                day_count += 1
        for col in range(1, COLUMNS):
            for row in range(ROWS):
                if day_count <= last_day:
                    buttons[row][col].config(text=str(day_count), state='normal')
                else:
                    buttons[row][col].config(text='', state='disabled')
                day_count += 1

    # Функция для увеличения месяца на 1
    def next_month():
        global current_date
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
        update_label()

    # Функция для уменьшения месяца на 1
    def prev_month():
        global current_date
        if current_date.month == 1:
            current_date = current_date.replace(year=current_date.year - 1, month=12)
        else:
            current_date = current_date.replace(month=current_date.month - 1)
        update_label()

    # Функция, которая вызывается при нажатии на кнопку
    def button_clicked(row, col):
        print(f"Кнопка нажата: ряд {row + 1}, столбец {col + 1}, текст: {buttons[row][col]['text']}")

    # Заголовки для дней недели
    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    tk.Label(canvas, text="ГРАФИК РАБОТЫ", font=("Arial", 30)).place(x=30, y=70)

    # Фрейм для сетки
    grid_frame = tk.Frame(canvas, width=GRID_WIDTH, height=GRID_HEIGHT)
    grid_frame.place(x=0, y=150)

    # Создание заголовков для дней недели (слева от таблицы)
    for col in range(ROWS):
        lbl = tk.Label(grid_frame, text=days_of_week[col], width=5, height=2, font=("Arial", 24))
        lbl.grid(row=col, column=0, sticky="nsew")  # Добавляем метки в первый столбец

    # Список для хранения кнопок
    buttons = []

    # Создание сетки из кнопок (с 1 столбца, т.к. 0 занят заголовками дней недели)
    for row in range(ROWS):
        button_row = []  # Список для хранения кнопок в текущем ряду
        for col in range(COLUMNS):
            btn = tk.Button(grid_frame, text=f"", font=("Arial", 24), width=6, height=2,
                            command=lambda r=row, c=col: button_clicked(r, c))
            btn.grid(row=row, column=col + 1, sticky="nsew")  # Сдвигаем на 1 столбец вправо
            button_row.append(btn)  # Добавляем кнопку в текущий ряд
        buttons.append(button_row)  # Добавляем ряд кнопок в общий список

    # Метки для отображения текущего месяца и диапазона дат
    month_label = tk.Label(canvas, font=("Arial", 20))
    month_label.place(x=300, y=900)

    range_label = tk.Label(canvas, font=("Arial", 14))
    range_label.place(x=300, y=940)

    # Кнопки для переключения месяцев
    prev_button = tk.Button(canvas, text="←", command=prev_month, width=10)
    prev_button.place(x=200, y=905)

    next_button = tk.Button(canvas, text="→", command=next_month, width=10)
    next_button.place(x=550, y=905)

    update_label()


# Размеры окна
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Размеры сетки (половина экрана)
GRID_WIDTH = WINDOW_WIDTH // 2
GRID_HEIGHT = WINDOW_HEIGHT // 2

# Количество колонок и строк (без учёта дней недели)
COLUMNS = 6
ROWS = 7

# Переменная для хранения текущего года и месяца
current_date = datetime.now()
months_ru = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]

if __name__ == '__main__':
    # Основное окно
    root = tk.Tk()
    root.title("Управление заказами")
    # Canvas для отображения выбранного текста
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    work_shedule(canvas)
    root.mainloop()
