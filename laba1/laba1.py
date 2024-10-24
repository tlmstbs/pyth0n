import random

def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    N = int(lines[0].strip())
    matrix = [list(map(int, line.strip().split())) for line in lines[1:]]
    return N, matrix

def generate_random_matrix(N, low=-10, high=10):
    return [[random.randint(low, high) for _ in range(N)] for _ in range(N)]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def in_area(i, j, N, area_num):
    if area_num == 1:
        return i > j and i + j < N - 1
    elif area_num == 2:
        return i < j and i + j < N - 1
    elif area_num == 3:
        return i < j and i + j > N - 1
    elif area_num == 4:
        return i > j and i + j > N - 1
    return False

def get_triangle_elements(matrix, N, area_num, count_elements=False):
    elements = []
    count_zeros = 0
    product_non_zeros = 1
    for i in range(N):
        for j in range(N):
            if in_area(i, j, N, area_num):
                elements.append(matrix[i][j])
                if count_elements:
                    if j%2!=0 and matrix[i][j] == 0:
                        count_zeros += 1
                    else:
                        product_non_zeros *= matrix[i][j]
    if count_elements:
        return elements, count_zeros, product_non_zeros
    return elements

def sym_replace_area_1_and_3(matrix, N, triangle_1, triangle_3):
    idx_1 = 0
    idx_3 = 0

    for i in range(N):
        for j in range(N):
            if in_area(i, j, N, 1):
                matrix[i][j] = triangle_3[idx_3]
                idx_3 += 1
            elif in_area(i, j, N, 3):
                matrix[i][j] = triangle_1[idx_1]
                idx_1 += 1
    return matrix

def asym_replace_area_2_and_3(matrix, N, triangle_2, triangle_3):
    idx_2 = 0
    idx_3 = 0

    for i in range(N):
        for j in range(N):
            if in_area(i, j, N, 2):
                matrix[i][j] = triangle_3[idx_3]
                idx_3 += 1
            elif in_area(i, j, N, 3):
                matrix[i][j] = triangle_2[-idx_2]
                idx_2 += 1
    return matrix

def matrix_t(matrix,N):
    return [[matrix[j][i]for j in range (N)]for i in range (N)]
def matrix_sum(matrix1, matrix2,N):
    return [[matrix1[i][j]+matrix2[i][j] for i in range(N)] for j in range(N)]
def matrix_multy_matrix(matrix1,matrix2,N):
    return [[matrix1[i][j] * matrix2[i][j] for i in range(N)] for j in range(N)]
def matrix_multy_k(matrix1,K,N):
    return [[matrix1[i][j] * K for i in range(N)] for j in range(N)]
def matrix_minus_matrix(matrix1,matrix2,N):
    return [[matrix1[i][j] - matrix2[i][j] for i in range(N)] for j in range(N)]

choice = input("Выберите метод заполнения матрицы (1 - случайное, 2 - из файла): ")

if choice == '1':
    N = int(input("Введите размер матрицы N (от 3 до 10): "))
    A = generate_random_matrix(N)
    print("Сгенерированная матрица A:")
    print_matrix(A)
elif choice == '2':
    file_path = "mat.txt"
    N, A = read_matrix_from_file(file_path)
    print("Матрица A из файла: ")
    print_matrix(A)
else:
    print("Неверный выбор")
    exit()

F = A.copy()

triangle_1 = get_triangle_elements(A, N, 1)
triangle_2, zero_count_2, _ = get_triangle_elements(A, N, 2, count_elements=True)
triangle_3 =get_triangle_elements(A, N, 3)
triangle_4, _, product_4 = get_triangle_elements(A, N, 4, count_elements=True)

print("\nТреугольник 1 (левый):", triangle_1)
print("Треугольник 2 (верхний):", triangle_2)
print("Треугольник 3 (правый):", triangle_3)
print("Треугольник 4 (нижний):", triangle_4)


if zero_count_2 > product_4:
    print("Выполняется симметричная замена областей 1 и 3")
    F = sym_replace_area_1_and_3(F, N, triangle_1, triangle_3)
else:
    print("Выполняется несимметричная замена областей 2 и 3")
    F = asym_replace_area_2_and_3(F, N, triangle_2, triangle_3)

print("\nМатрица F после замены:")
print_matrix(F)
K=int(input("Введите коэффицент К: "))
print("A*(F+A)-K*Ft")
ms=matrix_sum(F,A,N)
multy=matrix_multy_matrix(A,ms,N)
mt=matrix_t(F,N)
mk=matrix_multy_k(mt,K,N)
answer=matrix_minus_matrix(multy, mk, N)
print_matrix(answer)