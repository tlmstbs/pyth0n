num_to_text = {
    '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
    '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять',
    'A': 'а', 'B': 'бэ', 'C': 'це', 'D': 'дэ', 'E': 'е', 'F': 'эф'
}


def is_hex_number(s):
    """Проверка, является ли строка шестнадцатеричным числом."""
    valid_chars = "0123456789ABCDEF"
    for char in s:
        if char.upper() not in valid_chars:
            return False
    return True


def hex_with_a_in_third_position(hex_numbers):
    """Фильтрует шестнадцатеричные числа, у которых третья справа цифра 'A'."""
    filtered_numbers = []
    for num in hex_numbers:
        if len(num) >= 3 and num[-3].upper() == 'A':
            filtered_numbers.append(num)
    return filtered_numbers


def convert_number_to_text(number):
    """Преобразует число в текстовое представление."""
    return ' '.join(num_to_text[char] for char in number)


def main():

    with open('input.txt', 'r') as file:
        data = file.read()


    tokens = data.split()
    hex_numbers = [token for token in tokens if is_hex_number(token)]

    
    filtered_numbers = hex_with_a_in_third_position(hex_numbers)

    if not filtered_numbers:
        print("Нет подходящих чисел.")
        return


    max_hex = max(filtered_numbers, key=lambda x: int(x, 16))

  
    max_hex_text = convert_number_to_text(max_hex)
    print("Максимальное число:", max_hex)
    print("Число прописью:", max_hex_text)


if __name__ == "__main__":
    main()
