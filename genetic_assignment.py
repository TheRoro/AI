import random
import numpy as np

def gen_coord(choice, actual):
    if(choice == 0):
        return (actual[0]+1, actual[1])
    if(choice == 1):
        return (actual[0], actual[1]+1)

# Esta funcion valida que la coordenada aleatoria no sea pared
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


def generate_matrix(n):
    mat = [ [ 0 for i in range(n) ] for j in range(n) ]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(i == 0 or j == 0 or i == n - 1 or j == n - 1):
                mat[i][j] = 1
    return mat

def generate_labyrinth(start, end, matrix):
    actual = start
    mat = np.array(matrix)
    mat[start[0]][start[1]] = 2
    path = [start]
    
    while actual != end:
        choice = random.randint(0, 1)
        if(valid_choice(choice, actual, matrix)):
            actual = gen_coord(choice, actual)
            mat[actual[0]][actual[1]] = 2
            path.append(actual)
    
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j] != 2 and mat[i][j] != 1):
                choice = random.uniform(0, 1)
                if(choice > .35):
                    mat[i][j] = 0
                else:
                    mat[i][j] = 1
    
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j] == 2):
                mat[i][j] = 0

    return mat, path
n=10
mat = generate_matrix(n)
mat, path = generate_labyrinth((1,1), (8,8), mat)


##initial population
#Definimos 0=no se mueve, 1=arriba, 2=abajo, 3=derecha, 4=izquierda
# limite de movimientos = len(path) * 2 

poblation = 30
class chromosome:
    def __init__(self):
        self.path = []
        self.fitness = 0

##TORNEO de la primera poblacion de 50
def get_fitness(chromosome):
    pos_ini = (1,1)
    pos_final = (n-2,n-2)
    for i in range(max_movimientos):
        movi = chromosome.path[i]
        if(movi == 0):
            chromosome.fitness = chromosome.fitness + 0
        elif(movi == 1):#ARRIBA
            nueva_pos = (pos_ini[0],pos_ini[1]-1)
            ##validation limites:
            if(nueva_pos[0] < 0 or nueva_pos[0] > n-1):
                chromosome.fitness = 99999
                break
            elif(nueva_pos[1] < 0 or nueva_pos[1] > n-1):
                chromosome.fitness = 99999
                break

            fitness = abs((pos_final[0]-nueva_pos[0]) + (pos_final[1] - nueva_pos[1]))
            if(mat[nueva_pos[0]][nueva_pos[1]] == 1):
                fitness = fitness + 69
            newFitness = chromosome.fitness + fitness
            chromosome.fitness = newFitness
            pos_ini = nueva_pos
        elif(movi == 2):#ABAJO
            nueva_pos = (pos_ini[0],pos_ini[1]+1)
            ##validation limites:
            if(nueva_pos[0] < 0 or nueva_pos[0] > n-1):
                chromosome.fitness = 99999
                break
            elif(nueva_pos[1] < 0 or nueva_pos[1] > n-1):
                chromosome.fitness = 99999
                break

            fitness = abs((pos_final[0]-nueva_pos[0]) + (pos_final[1] - nueva_pos[1]))
            if(mat[nueva_pos[0]][nueva_pos[1]] == 1):
                fitness = fitness + 69
            newFitness = chromosome.fitness + fitness
            chromosome.fitness = newFitness
            pos_ini = nueva_pos
        elif(movi == 3):#DERECHA
            nueva_pos = (pos_ini[0]+1,pos_ini[1])
            ##validation limites:
            if(nueva_pos[0] < 0 or nueva_pos[0] > n-1):
                chromosome.fitness = 99999
                break
            elif(nueva_pos[1] < 0 or nueva_pos[1] > n-1):
                chromosome.fitness = 99999
                break

            fitness = abs((pos_final[0]-nueva_pos[0]) + (pos_final[1] - nueva_pos[1]))
            if(mat[nueva_pos[0]][nueva_pos[1]] == 1):
                fitness = fitness + 69
            newFitness = chromosome.fitness + fitness
            chromosome.fitness = newFitness
            pos_ini = nueva_pos
        elif(movi == 4):#IZQUIERDA
            nueva_pos = (pos_ini[0]-1,pos_ini[1])
            ##validation limites:
            if(nueva_pos[0] < 0 or nueva_pos[0] > n-1):
                chromosome.fitness = 99999
                break
            elif(nueva_pos[1] < 0 or nueva_pos[1] > n-1):
                chromosome.fitness = 99999
                break

            fitness = abs((pos_final[0]-nueva_pos[0]) + (pos_final[1] - nueva_pos[1]))
            if(mat[nueva_pos[0]][nueva_pos[1]] == 1):
                fitness = fitness + 69
            newFitness = chromosome.fitness + fitness
            chromosome.fitness = newFitness
            pos_ini = nueva_pos
    return chromosome

def fitness_score(chromosomes):
    for e in chromosomes:
        e = get_fitness(e)
    
    chromosomes.sort(key=lambda x: x.fitness)
    return chromosomes

#EMPIEZA EL TORNEO
def torneo(chromosomes):
    for k in range(0, poblation, 2):
        if(chromosomes[k].fitness > chromosomes[k+1].fitness):
            chromosomes[k] = chromosomes[k+1]
        else:
            chromosomes[k+1] = chromosomes[k]
    return chromosomes

#realizamos el real cruce
def crossover(chromosomes):
    random.shuffle(chromosomes)
    for e in chromosomes:
        print(e.path, e.fitness)

    for i in range(0, poblation, 2):
        pcruce = random.randint(0, max_movimientos - 2) + 1
        print("Punto de Cruce: ", pcruce)
        temp1 = chromosomes[i].path[:pcruce]
        temp2 = chromosomes[i+1].path[:pcruce]
        temp3 = chromosomes[i].path[pcruce:]
        temp4 = chromosomes[i+1].path[pcruce:]

        aux1 = temp1 + temp4
        aux2 = temp2 + temp3
        chromoAux = chromosome()
        chromoAux.path = aux1
        chromoAux2 = chromosome()
        chromoAux2.path = aux2
        chromosomes[i] = chromoAux
        chromosomes[i+1] = chromoAux2
        print("Nuevo Cromosoma en i", chromosomes[i].path)
        print("Nuevo Cromosoma en i + 1", chromosomes[i+1].path)

    return chromosomes
    
def mutation(chromosomes):
    for i in range(poblation):   
        prob = random.randint(0,1)
        print("probabilidad", prob)
        if(prob):
            posi = random.randint(0,max_movimientos-1)
            new_direction = random.randint(0,4)
            print("posi", posi, "direction", new_direction)
            chromosomes[i].path[posi] = new_direction
    return chromosomes

#inicializacion
#iniciamos la poblacion con los primeros 50 cromosomas
max_movimientos =  n*4
print("MOVIMIENTOS MAXIMOS: ", max_movimientos)
print("POBLACION: ", poblation)
chromosomes = []


for i in range(poblation):
    item = chromosome()
    for j in range(max_movimientos):
        direction = random.randint(0,4)
        item.path.append(direction)
    chromosomes.append(item)

chromosomes = fitness_score(chromosomes)
#tomamos los 6 primeros para el torneo
chromosomes_torneo = []
for i in range(poblation):
    chromosomes_torneo.append(chromosomes[i])

chromosomes = chromosomes_torneo


#GENERACIONES
for i in range(300):

    #POBLACION AL INICIO DE LA ITERACION
    for e in chromosomes:
        print(e.path, e.fitness)
    random.shuffle(chromosomes)

    print("i = ", i)
    #TORNEO
    print("TORNEO")
    chromosomes = torneo(chromosomes)

    for e in chromosomes:
        print(e.path, e.fitness)

    #CRUCE
    print("CRUCE")
    chromosomes = crossover(chromosomes)

    for e in chromosomes:
        print(e.path, e.fitness)

    #MUTATION
    print("MUTATION")
    chromosomes = mutation(chromosomes)

    for e in chromosomes:
        print(e.path, e.fitness)

    #RECALCULAMOS NUEVO FITNESS y mostramos poblacion final
    print("5 mejores GENES FINALES")
    chromosomes = fitness_score(chromosomes)
    for e in range(5):
        print(chromosomes[e].path, chromosomes[e].fitness)

    print("_____________________________________________________\n")


print("MAPA")
for e in mat:
    print(e)
print("\n")

posi_ini = (1,1)
mat[1][1] = 9
for i in range(max_movimientos):
    movimiento = chromosomes[0].path[i]
    print(posi_ini)
    if(movimiento == 1):
        posi = (posi_ini[0],posi_ini[1]-1)
        mat[posi[0]][posi[1]]=9
        posi_ini = posi
    if(movimiento == 2):
        posi = (posi_ini[0],posi_ini[1]+1)
        mat[posi[0]][posi[1]]=9
        posi_ini = posi
    if(movimiento == 3):
        posi = (posi_ini[0]+1,posi_ini[1])
        mat[posi[0]][posi[1]]=9
        posi_ini = posi
    if(movimiento == 4):
        posi = (posi_ini[0]-1,posi_ini[1])
        mat[posi[0]][posi[1]]=9
        posi_ini = posi

for e in mat:
    print(e)

    




