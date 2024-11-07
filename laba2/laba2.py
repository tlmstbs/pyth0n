import numpy as np
import matplotlib.pyplot as plt


def submatrix_random(s):
    subB =np.random.randint(-10,10,size=(s,s))
    subC = np.random.randint(-10, 10, size=(s, s))
    subD = np.random.randint(-10, 10, size=(s, s))
    subE = np.random.randint(-10, 10, size=(s, s))
    return subB,subC,subD,subE
def submatrix_txt():
    with open('matrix.txt', 'r') as file:
        lines = file.readlines()
    matrices = []
    current_matrix = []
    for line in lines:
        if line.strip():
            current_matrix.append([int(num) for num in line.split()])
        else:
            if current_matrix:
                matrices.append(np.array(current_matrix))
                current_matrix = []
    if current_matrix:
        matrices.append(np.array(current_matrix))
    return matrices
def submatrix_gen(size):
    s = (size, size)
    subB = np.full(s, 1)
    subC = np.full(s, 2)
    subD = np.full(s, 3)
    subE = np.full(s, 4)
    return subB, subC, subD, subE
def matrixfromsub(b,c,d,e):
    m1=np.concatenate((b,e),axis=1)
    m2 = np.concatenate((c, d), axis=1)
    m3 = np.concatenate((m1, m2), axis=0)
    return m3
def comparsion(sub):
    top=sub[0,:]
    bottom=sub[-1,:]
    left=sub[1:-1,0]
    right=sub[1:-1,-1]
    perimetr=np.concatenate([top, bottom, left, right])
    return np.sum(perimetr==0)
def matrixf(b,c,d,e):
    if comparsion(c)>0:
        m1 = np.concatenate((b, c), axis=1)
        m2 = np.concatenate((e, d), axis=1)
        m3 = np.concatenate((m1, m2), axis=0)
        return m3
    else:
        b2=np.flip(b)
        c2=np.sort(c)
        m1 = np.concatenate((c2, e), axis=1)
        m2 = np.concatenate((b2, d), axis=1)
        m3 = np.concatenate((m1, m2), axis=0)
        return m3
def example(ma,mf,k):
    g=np.tril(ma)
    deta=np.linalg.det(ma)
    if deta==0:
        ma_inv=np.linalg.pinv(ma)
        mf_inv = np.linalg.pinv(mf)
    else:
        ma_inv = np.linalg.inv(ma)
        mf_inv = np.linalg.inv(mf)
    if np.linalg.det(ma)>(sum(np.diagonal(mf))+sum(np.fliplr(mf).diagonal())):
        print("A-1*At-k*F")
        return (ma_inv*np.linalg.det(ma))-(k*mf)
    else:
        print("(A+g-F-1)*k")
        return(ma+g-mf_inv)*k
def column_means(matrix):
    col_means = np.mean(matrix, axis=0)
    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(len(col_means)), col_means)
    plt.title("Среднее значение по столбцам матрицы")
    plt.xlabel("Индекс столбца")
    plt.ylabel("Среднее значение")
    plt.grid(True)
def row_means(matrix):
    row_means = np.mean(matrix, axis=1)
    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(len(row_means)), row_means)
    plt.title("Среднее значение по строкам матрицы")
    plt.xlabel("Индекс строки")
    plt.ylabel("Среднее значение")
    plt.grid(True)
def heatmap(matrix):
    plt.figure(figsize=(6, 4))
    plt.imshow(matrix, cmap='plasma', interpolation='nearest')
    plt.colorbar(label='Значения матрицы')
    plt.title("Тепловая карта матрицы")
    plt.xlabel("Индекс столбца")
    plt.ylabel("Индекс строки")
while True:
    ch=int(input("Создание матрицы\n1-рандомом\n2-генератором\n3-из файла\nВаш выбор: "))
    if ch==1:
        s=int(input("Размер матрицы: "))
        subB,subC,subD,subE=submatrix_random(s)
        ma=matrixfromsub(subB,subC,subD,subE)
        break
    elif ch==2:
        s = int(input("Размер матрицы: "))
        subB, subC, subD, subE = submatrix_gen(s)
        ma = matrixfromsub(subB, subC, subD, subE)
        break
    elif ch==3:
        subB = submatrix_txt()[0]
        subC = submatrix_txt()[1]
        subD = submatrix_txt()[2]
        subE = submatrix_txt()[3]
        ma = matrixfromsub(subB, subC, subD, subE)
        break
print("матрица А")
print(ma)
mf=matrixf(subB, subC, subD, subE)
print("матрица F")
print(mf)
k=int(input("Введите коэффициент: "))
an=example(ma, mf, k)
print(an)
column_means(an)
row_means(an)
heatmap(an)
plt.show()