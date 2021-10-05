import random
n_indiv = 6
posis = [0, 1, 2, 3, 4, 5]

class Individual(object):
    def __init__(self, idy, x, fx, binary):
        self.id = idy
        self.x = x
        self.fx = fx
        self.binary = binary

def convert_binary(x):
    bina = bin(x)
    bina = bina[2:]
    n = (5 - len(bina)) * "0"
    bina = n + bina
    return bina

def generate_random(numbers):
    numbers = [10, 21, 6, 12, 7, 25]
    # while(len(numbers) < n_indiv):
    #     x = random.randint(0, 31)
    #     numbers.add(x)
    return numbers

def invert(string, pos):
    s = []
    for i in range(len(string)):
        if(i != pos):
            s.append(string[i])
        else:
            if(string[i] == "0"):
                s.append("1")
            else:
                s.append("0")
    return "".join(s)

def print_chart(indiv_list):
    print("ID \tBin \tX \tf(X)")
    for e in indiv_list:
        print(e.id, e.binary, e.x, e.fx, sep="\t")
    print("")
    
def print_chart_max_prom(indiv_list):
    maxi = 0
    acum = 0
    print("ID \tBin \tX \tf(X)")
    for e in indiv_list:
        maxi = max(maxi, e.fx)
        acum+=e.fx
        print(e.id, e.binary, e.x, e.fx, sep="\t")
    print("El mayor es:", maxi)
    print("El promedio es:", round(acum/len(indiv_list), 2))
    print("")

def print_pos(new_indiv_list, pos_list):
    print("ID \tBin \tX \tf(X) \tPos")
    j = 0
    for e in new_indiv_list:
        if(pos_list[j] == -1):
            print(e.id, e.binary, e.x, e.fx,"-", sep="\t")
        else:
            print(e.id, e.binary, e.x, e.fx, pos_list[j]+1, sep="\t")
        j+=1
    print("")

def init_indiv():
    indiv_list = []
    i = 0
    numbers = set()
    numbers = generate_random(numbers)
    for x in numbers:
        fx = x**3-21*x**2-3*x+150
        bina = convert_binary(x)
        indiv = Individual(i+1, x, fx, bina)
        indiv_list.append(indiv)
        i+=1
    return indiv_list

def tourn_select(indiv_list):
    random.shuffle(posis)
    print("Parejas:")
    for i in range(0, n_indiv, 2):
        print(posis[i]+1, "con", posis[i+1]+1)
    
    new_indiv_list = []
    for i in range(0, n_indiv, 2):
        if(indiv_list[posis[i]].fx > indiv_list[posis[i+1]].fx):
            copy = indiv_list[posis[i]]
        else:
            copy = indiv_list[posis[i+1]]
        indiv1 = Individual(i+1, copy.x,copy.fx, copy.binary)
        indiv2 = Individual(i+2, copy.x,copy.fx, copy.binary)

        new_indiv_list.append(indiv1)
        new_indiv_list.append(indiv2)
    return new_indiv_list

def cruce(new_indiv_list):
    random.shuffle(posis)
    list_cruces = []
    for i in range(0, n_indiv, 2):
        pcruce = random.randint(0, n_indiv - 2)
        list_cruces.append(pcruce)
        list_cruces.append(pcruce)

    print("Parejas:")
    for i in range(0, n_indiv, 2):
        print(posis[i]+1, "con", posis[i+1]+1)
        print("Punto de cruce", list_cruces[i])

    new_indiv_list_cruce = []
    print_chart(new_indiv_list)

    for i in range(0, n_indiv, 2):
        pcruce = list_cruces[posis[i]]
        temp1 = new_indiv_list[posis[i]].binary 
        temp2 = new_indiv_list[posis[i+1]].binary

        t1s1, t1s2 = temp1[:pcruce], temp1[pcruce:]
        t2s1, t2s2 = temp2[:pcruce], temp2[pcruce:]

        temp1 = t1s1 + t2s2
        temp2 = t2s1 + t1s2

        x1 = int(temp1,2)
        x2 = int(temp2,2)
        indiv1 = Individual(i+1, x1,x1**3-21*x1**2-3*x1+150, temp1)
        indiv2 = Individual(i+2, x2,x2**3-21*x2**2-3*x2+150, temp2)
        new_indiv_list_cruce.append(indiv1)
        new_indiv_list_cruce.append(indiv2)
    
    return new_indiv_list_cruce

def mutation(new_indiv_list):
    i = 0
    final_list = []
    pos_list = []
    for indiv in new_indiv_list:
        choice = random.randint(0, 3)
        if(choice == 1):
            pos = random.randint(0, n_indiv - 2)
            pos_list.append(pos)
            temp = invert(indiv.binary, pos)
            num = int(temp,2)
            indiv = Individual(i+1, int(temp,2),num**3-21*num**2-3*num+150, temp)
            final_list.append(indiv)
        else:
            pos_list.append(-1)
            final_list.append(indiv)
        i+=1
    
    print_pos(new_indiv_list, pos_list)
    return final_list


print("\n1. INICIALIZACIÓN:")
indiv_list = init_indiv()
print_chart_max_prom(indiv_list)

print("2. SELECCIÓN POR TORNEO:")
new_indiv_list = tourn_select(indiv_list)
print_chart(new_indiv_list)

print("3. CRUCE:")
new_indiv_list = cruce(new_indiv_list)
print_chart(new_indiv_list)

print("4. MUTACIÓN:")
final_list = mutation(new_indiv_list)
print_chart_max_prom(final_list)    