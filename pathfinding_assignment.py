from heapq import heappush, heappop
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import copy
from tkinter import *
from PIL import ImageTk, Image

# mat numbers:
# 0: Nodo no visitado
# 1: Pared
# 2: Visitado
# 3: Camino más corto

start = (1,1)
class chromosome:
    def __init__(self):
        self.path = []
        self.fitness = 0

def show_graphic(mat, cmap, title):
    fig, ax = plt.subplots(figsize=(5,5))
    ax.imshow(mat, interpolation='nearest')
    im = ax.imshow(mat,cmap=cmap)
    fig.colorbar(im)
    plt.title(title)
    plt.show()

def add_path_to_mat(path, mat):
    new_mat = copy.deepcopy(mat)
    for coord in path:
        X, Y = coord
        new_mat[X][Y] = 3
    return new_mat

# Esta función genera una matriz con paredes en los bordes
def generate_matrix(n):
    mat = [ [ 0 for i in range(n) ] for j in range(n) ]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(i == 0 or j == 0 or i == n - 1 or j == n - 1):
                mat[i][j] = 1
    return mat

# Esta funcion genera una coordenada
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

# Esta funcion genera un laberinto aleatorio con al menos 1 solución
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
                choice = random.uniform(0, 1)
                if(choice > .35):
                    mat[i][j] = 0
                else:
                    mat[i][j] = 1
    
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j] == 2):
                mat[i][j] = 0

    return mat

# Esta funcion genera una heurística en base a una matriz
def din_h(coordF, n):
    h_ini = [ [ 0 for i in range(n) ] for j in range(n) ]
    x, y = coordF
    h = copy.deepcopy(h_ini)
    col=len(h)
    row=len(h[0])
    for i in range(row):
        for j in range(col):
            if i == 0 or i == row-1:
                h[i][j] = -1
            elif j == 0 or j == col-1:
                h[i][j] = -1
            else:
                h[i][j] = (abs(i-x) + abs(j-y))*10

    return h

# Esta funcion valida que la coordenada generada no sea pared
def valid_coordinate(coord, mat):
    X, Y = coord
    if(mat[X][Y] != 1):
        return True
    return False

def valid_coordinate_best(coord, mat):
    X, Y = coord
    if(mat[X][Y] != 1 and mat[X][Y] != 2):
        return True
    return False

# Esta funcion genera una lista de hijos verticales/horizontales adyacentes al nodo visitado
def straight_children_best(coord, mat):
    # Only 4 children per node just vertical and horizontal movement
    X, Y = coord
    children = []
    
    posible = (X+1, Y)
    if(valid_coordinate_best(posible, mat)):
        children.append(posible)

    posible = (X, Y+1)
    if(valid_coordinate_best(posible, mat)):
        children.append(posible)

    posible = (X-1, Y)
    if(valid_coordinate_best(posible, mat)):
        children.append(posible)

    posible = (X, Y-1)
    if(valid_coordinate_best(posible, mat)):
        children.append(posible)

    return children

# Esta funcion genera una lista de hijos verticales/horizontales adyacentes al nodo visitado
def straight_children(coord, mat):
    # Only 4 children per node just vertical and horizontal movement
    X, Y = coord
    children = []
    
    posible = (X+1, Y)
    if(valid_coordinate(posible, mat)):
        children.append(posible)

    posible = (X, Y+1)
    if(valid_coordinate(posible, mat)):
        children.append(posible)

    posible = (X-1, Y)
    if(valid_coordinate(posible, mat)):
        children.append(posible)

    posible = (X, Y-1)
    if(valid_coordinate(posible, mat)):
        children.append(posible)

    return children

# Esta función construye el camino más corto generado por A estrella
def get_path(pred, end):
    path = []
    v = end
    while v != None:
        path.append(v)
        v = pred[v[0]][v[1]]
    path.reverse()
    return path

##TORNEO de la primera poblacion de 50
def get_fitness(chromosome, n, max_movimientos, mat):
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

def fitness_score(chromosomes, n, max_movimientos, mat):
    for e in chromosomes:
        e = get_fitness(e, n, max_movimientos, mat)
    
    chromosomes.sort(key=lambda x: x.fitness)
    return chromosomes

#EMPIEZA EL TORNEO
def torneo(chromosomes, poblation):
    for k in range(0, poblation, 2):
        if(chromosomes[k].fitness > chromosomes[k+1].fitness):
            chromosomes[k] = chromosomes[k+1]
        else:
            chromosomes[k+1] = chromosomes[k]
    return chromosomes

#realizamos el real cruce
def crossover(chromosomes, poblation, max_movimientos):
    random.shuffle(chromosomes)
    # for e in chromosomes:
    #     print(e.path, e.fitness)

    for i in range(0, poblation, 2):
        pcruce = random.randint(0, max_movimientos - 2) + 1
        # print("Punto de Cruce: ", pcruce)
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
        # print("Nuevo Cromosoma en i", chromosomes[i].path)
        # print("Nuevo Cromosoma en i + 1", chromosomes[i+1].path)

    return chromosomes

def mutation(chromosomes, poblation, max_movimientos):
    for i in range(poblation):   
        prob = random.randint(0,1)
        # print("probabilidad", prob)
        if(prob):
            posi = random.randint(0,max_movimientos-1)
            new_direction = random.randint(0,4)
            # print("posi", posi, "direction", new_direction)
            chromosomes[i].path[posi] = new_direction
    return chromosomes

def dijkstra(mat, start, end):
    n = len(mat)
    mat[start[0]][start[1]] = 2 # visited
    inf = 10**5
    finish = False # To break when the end node is found
    dist = [ [ inf for i in range(n) ] for j in range(n) ]
    pred = [ [ None for i in range(n) ] for j in range(n) ]
    dist[start[0]][start[1]] = 0
    q = []
    heappush(q, (dist[start[0]][start[1]], start[0], start[1]))

    while q and finish == False:
        obj = heappop(q)
        coord = (obj[1], obj[2])
        s_children = straight_children(coord, mat)
        XF = coord[0] # X coordinate of father
        YF = coord[1] # Y coordinate of father

        for e in s_children:
            XC = e[0] # X coordinate of child
            YC = e[1] # Y coordinate of child
            child_dist = dist[XC][YC] # The actual distance of the child
            new_dist = dist[XF][YF] + 1 # The posible new distance

            if(new_dist < child_dist):
                dist[XC][YC] = new_dist # Update min distance
                mat[XC][YC] = 2 # Node visited
                heappush(q, (new_dist, XC, YC)) # Add new node to the Priority Queue to search for its children
                pred[XC][YC] = coord # Update predecesor matrix

            if(e == end):
                finish = True
        
    return mat, pred, dist

def best_first_algorithm(mat, start, end, h):
    n = len(mat)
    mat[start[0]][start[1]] = 2 # visited
    inf = 10**5
    finish = False # To break when the end node is found
    dist = [ [ inf for i in range(n) ] for j in range(n) ]
    pred = [ [ None for i in range(n) ] for j in range(n) ]
    dist[start[0]][start[1]] = 0
    q = []
    heappush(q, (h[start[0]][start[1]], start[0], start[1]))
    while q and finish == False:
        obj = heappop(q)
        coord = (obj[1], obj[2])
        s_children = straight_children_best(coord, mat)
        XF = coord[0] # X coordinate of father
        YF = coord[1] # Y coordinate of father

        for e in s_children:
            XC = e[0] # X coordinate of child
            YC = e[1] # Y coordinate of child

            if(h[XC][YC] < h[XF][YF]):
                dist[XC][YC] = h[XF][YF] # Update min distance
                mat[XC][YC] = 2 # Node visited
                heappush(q, (h[XF][YF], XC, YC)) # Add new node to the Priority Queue to search for its children
                pred[XC][YC] = coord # Update predecesor matrix

            if(e == end):
                finish = True
        
    return mat, pred, dist

# Esta funcion es la lógica del algoritmo A estrella aplicada a una matriz (laberinto)
def a_star_mat(mat, start, end, h):
    n = len(mat)
    mat[start[0]][start[1]] = 2 # visited
    inf = 10**5
    finish = False # To break when the end node is found
    dist = [ [ inf for i in range(n) ] for j in range(n) ]
    pred = [ [ None for i in range(n) ] for j in range(n) ]
    dist[start[0]][start[1]] = 0
    q = []
    heappush(q, (h[start[0]][start[1]], start[0], start[1]))

    while q and finish == False:
        obj = heappop(q)
        coord = (obj[1], obj[2])
        s_children = straight_children(coord, mat)
        XF = coord[0] # X coordinate of father
        YF = coord[1] # Y coordinate of father

        for e in s_children:
            XC = e[0] # X coordinate of child
            YC = e[1] # Y coordinate of child
            child_dist = dist[XC][YC] # The actual distance of the child
            new_dist = dist[XF][YF] + 10 # The posible new distance

            if(new_dist + h[XF][YF] < child_dist + h[XC][YC]):
                dist[XC][YC] = new_dist # Update min distance
                mat[XC][YC] = 2 # Node visited
                heappush(q, (new_dist + h[XC][YC], XC, YC)) # Add new node to the Priority Queue to search for its children
                pred[XC][YC] = coord # Update predecesor matrix

            if(e == end):
                finish = True
        
    return mat, pred, dist

def genetic_algorithm(mat, n, genSize):
    # initial population
    # Definimos 0=no se mueve, 1=arriba, 2=abajo, 3=derecha, 4=izquierda
    # limite de movimientos = len(path) * 2 
    poblation = 30
    
    #inicializacion
    #iniciamos la poblacion con los primeros 50 cromosomas
    max_movimientos =  n*4
    # print("MOVIMIENTOS MAXIMOS: ", max_movimientos)
    # print("POBLACION: ", poblation)
    chromosomes = []

    for i in range(poblation):
        item = chromosome()
        for j in range(max_movimientos):
            direction = random.randint(0,4)
            item.path.append(direction)
        chromosomes.append(item)

    chromosomes = fitness_score(chromosomes, n, max_movimientos, mat)
    #tomamos los 6 primeros para el torneo
    chromosomes_torneo = []
    for i in range(poblation):
        chromosomes_torneo.append(chromosomes[i])

    chromosomes = chromosomes_torneo
    
    #GENERACIONES
    for i in range(genSize):
        print("Generación:", i+1)
        #POBLACION AL INICIO DE LA ITERACION
        # for e in chromosomes:
        #     print(e.path, e.fitness)
        random.shuffle(chromosomes)

        # print("i = ", i)
        # #TORNEO
        # print("TORNEO")
        chromosomes = torneo(chromosomes, poblation)

        # for e in chromosomes:
        #     print(e.path, e.fitness)

        #CRUCE
        # print("CRUCE")
        chromosomes = crossover(chromosomes, poblation, max_movimientos)

        # for e in chromosomes:
        #     print(e.path, e.fitness)

        #MUTATION
        # print("MUTATION")
        chromosomes = mutation(chromosomes, poblation, max_movimientos)

        # for e in chromosomes:
        #     print(e.path, e.fitness)

        #RECALCULAMOS NUEVO FITNESS y mostramos poblacion final
        # print("5 mejores GENES FINALES")
        chromosomes = fitness_score(chromosomes, n, max_movimientos, mat)
        # for e in range(5):
        #     print(chromosomes[e].path, chromosomes[e].fitness)

        # print("_____________________________________________________\n")

    # print("MAPA")
    # for e in mat:
    #     print(e)
    # print("\n")

    posi_ini = (1,1)
    mat[1][1] = 3
    for i in range(max_movimientos):
        movimiento = chromosomes[0].path[i]
        # print(posi_ini)
        if(movimiento == 1):
            posi = (posi_ini[0],posi_ini[1]-1)
            mat[posi[0]][posi[1]]=3
            posi_ini = posi
        if(movimiento == 2):
            posi = (posi_ini[0],posi_ini[1]+1)
            mat[posi[0]][posi[1]]=3
            posi_ini = posi
        if(movimiento == 3):
            posi = (posi_ini[0]+1,posi_ini[1])
            mat[posi[0]][posi[1]]=3
            posi_ini = posi
        if(movimiento == 4):
            posi = (posi_ini[0]-1,posi_ini[1])
            mat[posi[0]][posi[1]]=3
            posi_ini = posi
    return mat

def a_star_event():
    # 1. Generar Laberinto
    matSize=inputMatSize.get("1.0","end-1c")
    m_size = int(matSize)
    mat = generate_matrix(m_size)
    endcoord = (len(mat)-2, len(mat)-2)
    lab = generate_labyrinth(start,endcoord,mat)
    lab_mat = copy.deepcopy(lab)

    # 2. Resolver con A Estrella
    n = len(lab)
    h = din_h(endcoord, n)
    mat, pred, _dist = a_star_mat(lab, start, endcoord, h)
    path = get_path(pred, endcoord)
    mat = add_path_to_mat(path, mat)
    
    # 3. Mostrar Laberinto
    cmap_labyrinth = ListedColormap(["#FFFFFF", "#0B3547"])
    show_graphic(lab_mat, cmap_labyrinth, 'Laberinto Aleatorio de ' + matSize + 'x' + matSize)

    # 4. Mostrar Solución A Estrella
    cmap = ListedColormap(["#FFFFFF", "#0B3547", "#40CEE3", "#FFFE6A"])
    show_graphic(mat, cmap, 'Solución usando A Estrella')

def best_first_event():
    # 1. Generar Laberinto
    matSize=inputMatSize.get("1.0","end-1c")
    m_size = int(matSize)
    mat = generate_matrix(m_size)
    endcoord = (len(mat)-2, len(mat)-2)
    lab = generate_labyrinth(start,endcoord,mat)
    lab_mat = copy.deepcopy(lab)

    # 2. Resolver con Best First
    n = len(lab)
    h = din_h(endcoord, n)
    mat, pred, _dist = best_first_algorithm(lab, start, endcoord, h)
    path = get_path(pred, endcoord)
    mat = add_path_to_mat(path, mat)

    # 3. Mostrar Laberinto
    cmap_labyrinth = ListedColormap(["#FFFFFF", "#0B3547"])
    show_graphic(lab_mat, cmap_labyrinth, 'Laberinto Aleatorio de ' + matSize + 'x' + matSize)

    # 4. Mostrar Solución Best First
    cmap = ListedColormap(["#FFFFFF", "#0B3547", "#40CEE3", "#FFFE6A"])
    show_graphic(mat, cmap, 'Solución usando Best First')

def dijkstra_event():
    # 1. Generar Laberinto
    matSize=inputMatSize.get("1.0","end-1c")
    m_size = int(matSize)
    mat = generate_matrix(m_size)
    endcoord = (len(mat)-2, len(mat)-2)
    lab = generate_labyrinth((1,1),endcoord,mat)
    lab_mat = copy.deepcopy(lab)

    # 2. Resolver con Dijsktra
    mat, pred, _dist = dijkstra(lab, start, endcoord)
    path = get_path(pred, endcoord)
    mat = add_path_to_mat(path, mat)
    
    # 3. Mostrar Laberinto
    cmap_labyrinth = ListedColormap(["#FFFFFF", "#0B3547"])
    show_graphic(lab_mat, cmap_labyrinth, 'Laberinto Aleatorio de ' + matSize + 'x' + matSize)

    # 4. Mostrar Solución Dijsktra
    cmap = ListedColormap(["#FFFFFF", "#0B3547", "#40CEE3", "#FFFE6A"])
    show_graphic(mat, cmap, 'Solución usando Dijsktra')

def genetic_event():
    # n = 10
    matSize = inputMatSize.get("1.0","end-1c")
    m_size = int(matSize)
    genSize = inputGenSize.get("1.0","end-1c")
    genSize = int(genSize)
    n = m_size
    mat = generate_matrix(n)
    mat = generate_labyrinth((1,1), (n-2,n-2), mat)
    lab_mat = copy.deepcopy(mat)
    mat = genetic_algorithm(mat, n, genSize)

    # 3. Mostrar Laberinto
    cmap_labyrinth = ListedColormap(["#FFFFFF", "#0B3547"])
    show_graphic(lab_mat, cmap_labyrinth, 'Laberinto Aleatorio de ' + matSize + 'x' + matSize)

    # 4. Mostrar Solución Dijsktra
    cmap = ListedColormap(["#FFFFFF", "#0B3547", "#40CEE3", "#FFFE6A"])
    genTitle = 'Solución usando Algoritmos Geneticos ' + str(genSize) + ' generaciones'
    show_graphic(mat, cmap, genTitle)
    # for e in mat:
    #     print(e)

def compare_events():
    # 1. Generar Laberinto
    matSize=inputMatSize.get("1.0","end-1c")
    m_size = int(matSize)
    mat = generate_matrix(m_size)
    genSize = inputGenSize.get("1.0","end-1c")
    genSize = int(genSize)

    endcoord = (len(mat)-2, len(mat)-2)
    lab = generate_labyrinth(start,endcoord,mat)
    lab_mat = copy.deepcopy(lab)
    lab_a_star = copy.deepcopy(lab)
    lab_dijsktra = copy.deepcopy(lab)
    lab_best = copy.deepcopy(lab)
    lab_genetic = copy.deepcopy(lab)

    # 2. Mostrar Laberinto
    cmap_labyrinth = ListedColormap(["#FFFFFF", "#0B3547"])
    show_graphic(lab_mat, cmap_labyrinth, 'Laberinto Aleatorio de ' + matSize + 'x' + matSize)

    n = len(lab)
    h = din_h(endcoord, n)
    cmap = ListedColormap(["#FFFFFF", "#0B3547", "#40CEE3", "#FFFE6A"])

    # 3. Resolver con A Estrella
    mat_a_star, pred_a_star, _dist_a_star = a_star_mat(lab_a_star, start, endcoord, h)
    path_a_star = get_path(pred_a_star, endcoord)
    mat_a_star = add_path_to_mat(path_a_star, mat_a_star)
    
    # 4. Mostar solución A Star
    show_graphic(mat_a_star, cmap, 'Solución usando A estrella')

    # 5. Resolver con Dijkstra
    mat_dijsktra, pred_dijsktra, _dist_dijsktra = dijkstra(lab_dijsktra, start, endcoord)
    path_dijsktra = get_path(pred_dijsktra, endcoord)
    mat_dijsktra = add_path_to_mat(path_dijsktra, mat_dijsktra)
    
    # 6. Mostar solución Dijkstra
    show_graphic(mat_dijsktra, cmap, 'Solución usando Dijsktra')

    # 7. Resolver con Best First
    mat_best, pred_best, _dist_best = best_first_algorithm(lab_best, start, endcoord, h)
    path_best = get_path(pred_best, endcoord)
    mat_best = add_path_to_mat(path_best, mat_best)
    
    # 8. Mostar Solución Best First
    show_graphic(mat_best, cmap, 'Solución usando Best First (Voraz)')

    # 9. Resolver con Algoritmo Genetico
    mat_genetic = genetic_algorithm(lab_genetic, n, genSize)

    # 8. Mostar con Algoritmo Genetico
    genTitle = 'Solución usando Algoritmos Geneticos ' + str(genSize) + ' generaciones'
    show_graphic(mat_genetic, cmap, genTitle)

root = Tk()
root.title('Labyrinth Solver')
root.geometry("400x400")

var = StringVar()
label = Label(root, textvariable=var, relief=FLAT)
var.set("Ingresar tamaño del laberinto:")
label.config(font=(16))
label.pack()

inputMatSize=Text(root, height=2, width=10)
inputMatSize.pack()

var2 = StringVar()
label2 = Label(root, textvariable=var2, relief=FLAT)
var2.set("Ingresar el numero de generaciones (Solo genetico):")
label2.config(width=200)
label2.pack()

inputGenSize=Text(root, height=1.5, width=10)
inputGenSize.pack()

# Botón para resolver con Best First
best_first_btn=Button(root, height=1, width=10, text="Best First", command=lambda: best_first_event())
best_first_btn.pack()

# Botón para resolver con A Estrella
a_star_btn=Button(root, height=1, width=10, text="A Estrella", command=lambda: a_star_event())
a_star_btn.pack()

# Botón para resolver con Dijkstra
dijkstra_btn=Button(root, height=1, width=10, text="Dijsktra", command=lambda: dijkstra_event())
dijkstra_btn.pack()

# REEMPLAZAR CON ALGORITMO NUEVO
genetic_btn=Button(root, height=1, width=10, text="Genetico", command=lambda: genetic_event())
genetic_btn.pack()

# Botón para comparar todos los algoritmos
compare_btn=Button(root, height=1, width=10, text="Comparar", command=lambda: compare_events())
compare_btn.pack()

root.mainloop()