import random
import numpy as np

def generate_matrix(n):
    mat = [ [ 0 for i in range(n) ] for j in range(n) ]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(i == 0 or j == 0 or i == n - 1 or j == n - 1):
                mat[i][j] = 1
    return mat

mat = generate_matrix(20)
for row in mat:
    print(row)

def gen_coord(choice, actual):
    if(choice == 0):
        return (actual[0]+1, actual[1])
    if(choice == 1):
        return (actual[0], actual[1]+1)

def valid_choice(choice, actual, mat):
    if(choice == 0):
        if(mat[actual[0]+1][actual[1]] == 0):
            return True
        else:
            return False
    elif(choice == 1):
        if(mat[actual[0]][actual[1]+1] == 0):
            return True
        else:
            return False

def generate_labyrinth(start, end, matrix):
    actual = start
    mat = np.array(matrix)
    mat[start[0]][start[1]] = 2
    
    while actual != end:
        choice = random.randint(0, 1)
        if(valid_choice(choice, actual, matrix)):
            actual = gen_coord(choice, actual)
            mat[actual[0]][actual[1]] = 2
    
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j] != 2 and mat[i][j] != 1):
                choice = random.randint(0, 1)
                mat[i][j] = choice
    
    ans = np.copy(mat)

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j] == 2):
                mat[i][j] = 0

    return ans, mat

endcoord = (len(mat)-2, len(mat)-2)

solution, labyrinth = generate_labyrinth((1,1),endcoord,mat)

for row in labyrinth:
    print(row)