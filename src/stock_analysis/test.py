def convert(n, m, i, j):
    return i * n + j


n, m = 4, 5
matrix = []
for i in range(n):
    matrix.insert(i, [])
    for j in range(m):
        matrix[i].insert(j, (i, j))
print(matrix)

matrix = []
for i in range(n):
    matrix.insert(i, [])
    for j in range(m):
        matrix[i].insert(j, convert(n, m, i, j))
print(matrix)
