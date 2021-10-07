class Item:
    def __init__(self, w, v):
        self.w = w
        self.v = v

class Node:
    def __init__(self, h = 0, b = 0, w = 0, l = None):
        self.w = w
        self.b = b
        self.h = h
        self.l = l

def enlace(x, n, m, listy):
    if (x.w >= m):
        return 0
    max_w = x.w
    b_link = x.b 
    a = x.h + 1
    while ((a < n) and (max_w + listy[a].w <= m)):
        max_w += listy[a].w
        b_link += listy[a].v
        a += 1
    if (a < n):
        b_link = b_link + (m - max_w) * listy[a].v / listy[a].w
    return b_link

def BranchAndBound(items, m, n):
    listy = []
    child = Node()
    father = Node(-1, 0, 0)
    listy.append(father)
    b_max = 0
    while (not len(listy) == 0):
        father = listy[-1]
        listy.pop()
        if (father.h == -1):
            child.h = 0
        if (father.h == n - 1):
            continue
        child.h = father.h + 1
        child.w = father.w + items[child.h].w
        child.b = father.b + items[child.h].v
        if (child.w <= m and child.b > b_max): 
            b_max = child.b
        child.l = enlace(child, n, m, items)
        if (child.l > b_max): 
            listy.insert(0, child)
        child.w = father.w
        child.b = father.b
        if (child.l > b_max):
            listy.insert(0, child)          
    return b_max

n = 4
items = [Item(8, 4), Item(12, 8), Item(16, 12), Item(20, 16)]
m = 28
print('El máximo beneficio para el problema es:', BranchAndBound(items, m, n))