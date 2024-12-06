"""Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно.
Определить границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной форме.
Обязательное требование – минимизация времени выполнения и объема памяти"""

import timeit
import math

def recursive_f_optimized(n):
    if n == 1:
        return 2
    elif n == 2:
        return 4
    else:
        factorial_3n = math.factorial(3 * n)
        m=-1 if n%2 else 1
        return m*  (recursive_f_optimized(n - 1) - recursive_f_optimized(n - 2) / factorial_3n)

def iterative_f_optimized(n):
    if n == 1:
        return 2
    elif n == 2:
        return 4
    f_prev2 = 2  # F(1)
    f_prev1 = 4  # F(2)
    m=-1
    for i in range(3, n + 1):
        factorial_3n = math.factorial(3*i)
        f_curr = m * (f_prev1 - f_prev2 / factorial_3n)
        m*=-1
        f_prev2, f_prev1 = f_prev1, f_curr
    return f_prev1

def compare_execution_times_and_limits(n):
    recursive_time = timeit.timeit(lambda: recursive_f_optimized(n), number=10) * 100
    iterative_time = timeit.timeit(lambda: iterative_f_optimized(n), number=10) * 100
    print(f"Результат рекурсии для n={n}: {recursive_f_optimized(n)}")
    print(f"Результат итерации для n={n}: {iterative_f_optimized(n)}")
    print(f"Время выполнения рекурсии: {recursive_time:.6f} секунд")
    print(f"Время выполнения итерации: {iterative_time:.6f} секунд")
n_values = int(input("Введите число: "))
compare_execution_times_and_limits(n_values)
