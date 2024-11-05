"""Лабораторная работа №5
Задана рекуррентная функция. Область определения функции – натуральные числа. 
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно. 
Определить границы применимости рекурсивного и итерационного подхода. 
Результаты сравнительного исследования времени вычисления представить в табличной форме. 
Обязательное требование – минимизация времени выполнения и объема памяти.


Вариант 28.	
F(1) = 2; F(2) = 4; F(n) = (-1)n*(F(n-1)-F(n-2) /(3n)!) при n > 2. """


import time
import math
from functools import lru_cache


@lru_cache(maxsize=None)
def recursive_f_optimized(n):
    if n == 1:
        return 2
    elif n == 2:
        return 4
    else:
        factorial_3n = math.factorial(3 * n)
        return (-1) ** n * (recursive_f_optimized(n - 1) - recursive_f_optimized(n - 2) / factorial_3n)


def iterative_f_optimized(n):
    if n == 1:
        return 2
    elif n == 2:
        return 4

    f_prev2 = 2  # F(1)
    f_prev1 = 4  # F(2)
    factorial_3n = math.factorial(3) 

    for i in range(3, n + 1):
        factorial_3n *= (3 * i - 2) * (3 * i - 1) * 3 * i
        f_curr = (-1) ** i * (f_prev1 - f_prev2 / factorial_3n)
        f_prev2, f_prev1 = f_prev1, f_curr

    return f_prev1


def compare_execution_times_and_limits(n_values, time_limit=1):
    results = []
    recursion_limit = None
    for n in n_values:
        start_time = time.time()
        try:
            recursive_result = recursive_f_optimized(n)
            recursive_time = time.time() - start_time
        except (RecursionError, OverflowError):
            recursive_result = "Recursion/Overflow Error"
            recursive_time = float('inf')
            if recursion_limit is None:
                recursion_limit = n - 1

        start_time = time.time()
        iterative_result = iterative_f_optimized(n)
        iterative_time = time.time() - start_time

        if recursive_time > time_limit and recursion_limit is None:
            recursion_limit = n - 1

        results.append((n, recursive_result, recursive_time, iterative_result, iterative_time))

    print(
        f"{'n':<10}{'Recursive Result':<20}{'Recursive Time (s)':<20}{'Iterative Result':<20}{'Iterative Time (s)':<20}")
    print("-" * 90)
    for result in results:
        n, rec_res, rec_time, iter_res, iter_time = result
        print(f"{n:<10}{rec_res:<20}{rec_time:<20.6f}{iter_res:<20}{iter_time:<20.6f}")

    print("\nГраницы применимости:")
    print(f"Максимальное значение n для рекурсивного подхода: {recursion_limit}")
    print("Итеративный подход работает для больших n, но может замедлиться при очень больших значениях.")


n_values = [1, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45]
compare_execution_times_and_limits(n_values)
