"""Задание на л.р. №6
Задание состоит из двух частей. 
1 часть – написать программу в соответствии со своим вариантом задания. 
Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.

2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение 
на характеристики объектов (которое будет сокращать количество переборов) и целевую функцию для нахождения оптимального  решения.


Вариант 28. Фирма занимается сборкой компьютеров. В компьютере компоненты N типов. 
На складе находятся компоненты разных компаний. Количество компаний К1, К2, … КN. Сформировать все возможные варианты комплектации компьютеров."""


import itertools
import time

N = 3
K = [2, 3, 2]

def generate_combinations_algorithmic(K):
    result = [[]]
    for companies in K:
        new_result = []
        for combination in result:
            for company in range(companies):
                new_result.append(combination + [company])
        result = new_result

    filtered_result = [combo for combo in result if len(set(combo)) == len(combo)]
    return filtered_result


def generate_combinations_python(K):
    ranges = [range(companies) for companies in K]
    all_combinations = list(itertools.product(*ranges))

    filtered_result = [combo for combo in all_combinations if len(set(combo)) == len(combo)]
    return filtered_result


def find_best_combination(combinations):
    max_unique_count = 0
    best_combination = None
    for combo in combinations:
        unique_count = len(set(combo))
        if unique_count > max_unique_count:
            max_unique_count = unique_count
            best_combination = combo
    return best_combination


start_time = time.time()
combinations_algo = generate_combinations_algorithmic(K)
algo_time = time.time() - start_time
print("Алгоритмический подход:", combinations_algo)
print("Время выполнения (алгоритмический):", algo_time)


start_time = time.time()
combinations_python = generate_combinations_python(K)
python_time = time.time() - start_time
print("Python-функции:", combinations_python)
print("Время выполнения (Python-функции):", python_time)


best_combination_algo = find_best_combination(combinations_algo)
best_combination_python = find_best_combination(combinations_python)

print("Лучшая комбинация (алгоритмический подход):", best_combination_algo)
print("Лучшая комбинация (Python-функции):", best_combination_python)
