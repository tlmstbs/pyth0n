"""Лабораторная работа №4
Написать программу, которая читая символы из файла, распознает, 
преобразует и выводит на экран объекты по определенному правилу. 
Объекты разделены пробелами. Распознавание и преобразование делать по возможности через регулярные выражения. 
Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа.

Вариант 28.
Шестнадцатеричные числа, у которых 3я справа цифра равна А. Максимальное число вывести прописью."""


import re

num_to_text = {
    '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
    '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять',
    'A': 'а', 'B': 'бэ', 'C': 'це', 'D': 'дэ', 'E': 'е', 'F': 'эф'
}


def find_hex_numbers_with_a(file_content):
    

    hex_pattern = r'\b[0-9A-Fa-f]+\b'
    hex_numbers = re.findall(hex_pattern, file_content)

    filtered_numbers = [num for num in hex_numbers if len(num) >= 3 and num[-3].upper() == 'A']
    return filtered_numbers


def convert_number_to_text(number):
   
    return ' '.join(num_to_text[char] for char in number.upper())


def main():
    with open('input.txt', 'r') as file:
        data = file.read()

    filtered_numbers = find_hex_numbers_with_a(data)

    if not filtered_numbers:
        print("Нет подходящих чисел.")
        return

    max_hex = max(filtered_numbers, key=lambda x: int(x, 16))

    max_hex_text = convert_number_to_text(max_hex)
    print("Максимальное число:", max_hex)
    print("Число прописью:", max_hex_text)


if __name__ == "__main__":
    main()
