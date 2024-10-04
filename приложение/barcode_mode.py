import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import aspose.barcode.generation as barcode
from tkinter import ttk


def barcode_mode(canvas):
    def print_marka(path):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(path, "print")
            else:
                # Для Linux или MacOS используем команду lp
                os.system(f"lp {path}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отправить на печать: {e}")

    def do_code():
        if table_dropdown.get() == valu[0]:
            generator_qr = barcode.BarcodeGenerator(barcode.EncodeTypes.CODE39)
        elif table_dropdown.get() == valu[1]:
            generator_qr = barcode.BarcodeGenerator(barcode.EncodeTypes.QR)
        elif table_dropdown.get() == valu[2]:
            generator_qr = barcode.BarcodeGenerator(barcode.EncodeTypes.DATA_MATRIX)
        else:
            generator_qr = barcode.BarcodeGenerator(barcode.EncodeTypes.QR)

        generator_qr.code_text = entry.get()
        generator_qr.save("код.jpg")
        img = Image.open("код.jpg")

        if table_dropdown.get() == valu[0]:
            img = img.resize(((len(entry.get())) * 20, 100), Image.LANCZOS)
        else:
            img = img.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        img_label.image = photo

    entry = tk.Entry(canvas, width=30)
    entry.place(x=1000, y=400)

    button1 = tk.Button(canvas, text="сформировать код", command=lambda: do_code())
    button1.place(x=550, y=100)

    button1 = tk.Button(canvas, text="Распечатать код", command=lambda: print_marka("код.jpg"))
    button1.place(x=550, y=200)

    img_label = tk.Label(canvas)
    img_label.place(x=500, y=500)

    table_dropdown = ttk.Combobox(canvas, state="readonly", font=("Arial", 12))
    table_dropdown.place(x=1000, y=350)
    valu = ["штрих-код", "qr-код", "марка"]
    table_dropdown['values'] = valu


if __name__ == '__main__':
    # Основное окно приложения
    root = tk.Tk()
    root.geometry('1920x1080')
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    barcode_mode(canvas)
    root.mainloop()
