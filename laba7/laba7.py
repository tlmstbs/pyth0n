"""Задание на л.р. №6
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания.
Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.

2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение
на характеристики объектов (которое будет сокращать количество переборов) и целевую функцию для нахождения оптимального  решения.


Вариант 28. Фирма занимается сборкой компьютеров. В компьютере компоненты N типов.
На складе находятся компоненты разных компаний. Количество компаний К1, К2, … КN. Сформировать все возможные варианты комплектации компьютеров."""


import tkinter as tk
from tkinter import scrolledtext
import itertools
import timeit

def generate_combinations_python(K, unique_only=True):
    ranges = [range(companies) for companies in K]
    all_combinations = list(itertools.product(*ranges))
    if unique_only:
        filtered_result = [combo for combo in all_combinations if len(set(combo)) == len(combo)]
        return filtered_result
    return all_combinations
def find_best_combination(combinations):
    max_unique_count = 0
    best_combination = None
    for combo in combinations:
        unique_count = len(set(combo))
        if unique_count > max_unique_count:
            max_unique_count = unique_count
            best_combination = combo
    return best_combination
def generate_and_display():
    try:
        n = int(entry_n.get())
        k_values = list(map(int, entry_k.get().split(',')))
        if len(k_values) != n:
            output_text.insert(tk.END, "Ошибка: количество элементов в K должно быть равно N\n")
            return
        def timer_func():
            return generate_combinations_python(k_values)
        python_time = timeit.timeit(timer_func, number=1)
        combinations_python = timer_func()
        if not combinations_python:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Нет уникальных комбинаций. Проверьте значения K.\n")
            return
        best_combination = find_best_combination(combinations_python)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Количество комбинаций: {len(combinations_python)}\n\n")
        output_text.insert(tk.END, f"Примеры комбинаций:\n")
        output_text.insert(tk.END, f"{combinations_python[:10]}\n\n")
        output_text.insert(tk.END, f"Время выполнения: {python_time:.6f} сек\n")
        output_text.insert(tk.END, f"Лучшая комбинация: {best_combination}\n")
    except ValueError:
        output_text.insert(tk.END, "Ошибка: Проверьте введённые значения. Ожидаются целые числа.\n")
root = tk.Tk()
root.title("Комплектация компьютеров")
frame_input = tk.Frame(root)
frame_input.pack(pady=10)
label_n = tk.Label(frame_input, text="Введите количество типов компонентов (N):")
label_n.grid(row=0, column=0, padx=5, pady=5)
entry_n = tk.Entry(frame_input, width=10)
entry_n.grid(row=0, column=1, padx=5, pady=5)
label_k = tk.Label(frame_input, text="Введите количество производителей для каждого типа через запятую (K):")
label_k.grid(row=1, column=0, padx=5, pady=5)
entry_k = tk.Entry(frame_input, width=30)
entry_k.grid(row=1, column=1, padx=5, pady=5)
button_generate = tk.Button(root, text="Сгенерировать комбинации", command=generate_and_display)
button_generate.pack(pady=10)
output_text = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
output_text.pack(padx=10, pady=10)
root.mainloop()
