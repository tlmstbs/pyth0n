"""
Требуется написать ООП с графическим интерфейсом в соответствии со своим вариантом.
Должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных не использовать. При необходимости сохранять информацию в файлах, разделяя значения запятыми (CSV файлы) или пробелами. Для GUI и визуализации использовать библиотеку tkinter.

Вариант 28
Объекты – библиотечные книги
Функции:	сегментация полного списка книг по учебным дисциплинам
визуализация предыдущей функции в форме круговой диаграммы
сегментация полного списка книг по использованию (часто, средне, редко, никогда)
визуализация предыдущей функции в форме круговой диаграммы


Пример файла:

Основы программирования,Информатика,часто
Алгоритмы и структуры данных,Информатика,средне
Математический анализ,Математика,редко
Физика,Физика,никогда
Операционные системы,Информатика,часто
Теория вероятностей,Математика,средне
Электродинамика,Физика,редко


"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import matplotlib.pyplot as plt
from docx import Document
import csv


class Library:
    def __init__(self):
        self.books = []

    def add_books_from_txt(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    title, subject, usage = line.strip().split(',')
                    self.books.append({"title": title, "subject": subject, "usage": usage})
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

    def add_books_from_docx(self, file_path):
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                parts = para.text.split(',')
                if len(parts) == 3:
                    title, subject, usage = parts
                    self.books.append({"title": title.strip(), "subject": subject.strip(), "usage": usage.strip()})
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

    def segment_by_subject(self):
        subjects = {}
        for book in self.books:
            subject = book["subject"]
            if subject not in subjects:
                subjects[subject] = 0
            subjects[subject] += 1
        return subjects

    def segment_by_usage(self):
        usage = {"часто": 0, "средне": 0, "редко": 0, "никогда": 0}


        for book in self.books:
            if book["usage"]:
                usage_key = book["usage"].strip().lower()  # Убираем пробелы и приводим к нижнему регистру
                if usage_key in usage:  # Проверяем, есть ли такой ключ в словаре
                    usage[usage_key] += 1
                else:
                    print(
                        f"Неверное значение для использования книги: {book['usage']}")  # Сообщаем о неправильном значении
            else:
                print(f"Отсутствует информация о частоте использования для книги: {book}")

        return usage


def display_pie_chart(data, title):
    labels = data.keys()
    sizes = data.values()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Word files", "*.docx")])
    if file_path:
        if file_path.endswith('.txt'):
            library.add_books_from_txt(file_path)
        elif file_path.endswith('.docx'):
            library.add_books_from_docx(file_path)
        else:
            messagebox.showerror("Ошибка", "Поддерживаются только .txt и .docx файлы.")
            return

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Загружено {len(library.books)} книг.\n")


def segment_by_subject():
    subjects = library.segment_by_subject()
    display_pie_chart(subjects, "Сегментация по учебным дисциплинам")


def segment_by_usage():
    usage = library.segment_by_usage()
    display_pie_chart(usage, "Сегментация по частоте использования")


root = tk.Tk()
root.title("Библиотека книг")

library = Library()

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

button_open = tk.Button(frame_input, text="Открыть файл", command=open_file)
button_open.grid(row=0, column=0, padx=10)

button_segment_subject = tk.Button(frame_input, text="Сегментация по дисциплинам", command=segment_by_subject)
button_segment_subject.grid(row=0, column=1, padx=10)

button_segment_usage = tk.Button(frame_input, text="Сегментация по использованию", command=segment_by_usage)
button_segment_usage.grid(row=0, column=2, padx=10)

output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.pack(padx=10, pady=10)

root.mainloop()
