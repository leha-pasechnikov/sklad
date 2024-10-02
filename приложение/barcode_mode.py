import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import aspose.barcode.generation as barcode

def barcode_mode(canvas):
    # Функции, которые будут вызываться при нажатии на кнопки
    def do_barcode(event):
        generator_barcode = barcode.BarcodeGenerator(barcode.EncodeTypes.CODE39)
        if ord(event.char) != 8:
            generator_barcode.code_text = entry1.get() + event.char
        else:
            if not (len(entry1.get()) == 1 and ord(event.char) == 8) and not (len(entry1.get()) == 0):
                generator_barcode.code_text = entry1.get()[:-1]
        generator_barcode.save("Barcode.jpg")
        update_image("Barcode.jpg", img_label1, event.char)


    def do_qr(event):
        generator_qr = barcode.BarcodeGenerator(barcode.EncodeTypes.QR)
        if ord(event.char) != 8:
            generator_qr.code_text = entry2.get() + event.char
        else:
            if not (len(entry2.get()) == 1 and ord(event.char) == 8) and not (len(entry2.get()) == 0):
                generator_qr.code_text = entry2.get()[:-1]
        generator_qr.save("qr.jpg")
        update_image("qr.jpg", img_label2, event.char)


    def do_marka(event):
        generator_marka = barcode.BarcodeGenerator(barcode.EncodeTypes.DATA_MATRIX)
        if ord(event.char) != 8:
            generator_marka.code_text = entry3.get() + event.char
        else:
            if not (len(entry3.get()) == 1 and ord(event.char) == 8) and not (len(entry3.get()) == 0):
                generator_marka.code_text = entry3.get()[:-1]
        generator_marka.save("marka.jpg")
        update_image("marka.jpg", img_label3, ord(event.char))


    # Функция для обновления изображений
    def update_image(image_path, label, ch):
        img = Image.open(image_path)
        if image_path == "Barcode.jpg":
            if ch==8:
                img = img.resize(((len(entry1.get()) + 3) * 20, 100), Image.LANCZOS)  # Изменение размера изображения
            elif ch==-1:
                img = img.resize((400, 100), Image.LANCZOS)  # Изменение размера изображения
            else:
                img = img.resize(((len(entry1.get()) + 4) * 20, 100), Image.LANCZOS)  # Изменение размера изображения
        else:
            print(len(entry3.get()))
            img = img.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo  # Сохранение ссылки на изображение, чтобы не было сборки мусора


    def print_marka(path):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(path, "print")
            else:
                # Для Linux или MacOS используем команду lp
                os.system(f"lp {path}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отправить на печать: {e}")




    # Поля ввода
    entry1 = tk.Entry(canvas, width=30)
    entry1.place(x=150, y=100)

    entry2 = tk.Entry(canvas, width=30)
    entry2.place(x=150, y=300)

    entry3 = tk.Entry(canvas, width=30)
    entry3.place(x=150, y=500)

    # Метки для изображений
    img_label1 = tk.Label(canvas)
    img_label1.place(x=500, y=100)
    update_image("Barcode.jpg", img_label1,-1)
    entry1.bind("<KeyPress>", do_barcode)

    img_label2 = tk.Label(canvas)
    img_label2.place(x=500, y=300)
    update_image("qr.jpg", img_label2,0)
    entry2.bind("<KeyPress>", do_qr)

    img_label3 = tk.Label(canvas)
    img_label3.place(x=500, y=500)
    update_image("marka.jpg", img_label3,0)
    entry3.bind("<KeyPress>", do_marka)

    # Кнопки
    button1 = tk.Button(canvas, text="Распечатать штрих-код", command=lambda: print_marka("Barcode.jpg"))
    button1.place(x=350, y=100)

    button2 = tk.Button(canvas, text="Распечатать QR-код", command=lambda: print_marka("qr.jpg"))
    button2.place(x=350, y=300)

    button3 = tk.Button(canvas, text="Распечатать марку", command=lambda: print_marka("marka.jpg"))
    button3.place(x=350, y=500)

if __name__=='__main__':
    # Основное окно приложения
    root = tk.Tk()
    root.geometry('1920x1080')
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    barcode_mode(canvas)
    root.mainloop()
