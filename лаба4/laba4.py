"""Лабораторная работа №3
Написать программу, которая читая символы из бесконечной последовательности (эмулируется
конечным файлом), распознает, преобразует и выводит на экран объекты по определенному правилу.
Объекты разделены пробелами. Преобразование делать по возможности через словарь. Для
упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр
числа. Регулярные выражения использовать нельзя.

Вариант 28.
Шестнадцатеричные числа, у которых 3я справа цифра равна А. Максимальное число вывести
прописью."""



import re

num_to_text = {
    '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
    '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять',
    'A': 'а', 'B': 'бэ', 'C': 'це', 'D': 'дэ', 'E': 'е', 'F': 'эф'
}

def has_a_in_third_position(num):
   
    return re.search(r'.*A[\dA-Fa-f]{2}$', num, re.IGNORECASE) is not None


def convert_number_to_text(number):
    if number[0] == '-':
        text = 'минус ' + ' '.join(num_to_text[char] for char in number[1:].upper())
    else:
        text = ' '.join(num_to_text[char] for char in number.upper())
    return text


with open('input.txt', 'r') as file:
    lines = file.readlines()
filtered_numbers = []

for line in lines:
    line = line.strip()
    hex_pattern = r'-?[0-9A-Fa-f]+'
    hex_numbers = re.findall(hex_pattern, line)

    for num in hex_numbers:
        if has_a_in_third_position(num):
            filtered_numbers.append(num)


if not filtered_numbers:
    print("Нет подходящих чисел.")
    exit(0)
    
decimal_values = [
    (num, int(num, 16) if num[0] != '-' else -int(num[1:], 16))
    for num in filtered_numbers
]

max_hex, _ = max(decimal_values, key=lambda x: x[1])

max_hex_text = convert_number_to_text(max_hex)
print("Максимальное число:", max_hex)
print("Число прописью:", max_hex_text)

