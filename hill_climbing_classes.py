import copy

class Option(object):
    def __init__(self, puzzle, h, x, y, xn, yn):
        self.puzzle = puzzle
        self.h = h
        self.x = x
        self.y = y
        self.xn = xn
        self.yn = yn

class HillClimb(object):
    def calculateH(self, puzzleA):
        cont = 0
        for i in range(3):
            for j in range(3):
                if puzzleA[i][j] != puzzle[i][j]:
                    cont = cont + 1
        return cont

    def setStartNode(self, puzzleA):
        x = 0
        y = 0
        for i in range(3):
            for j in range(3):
                if puzzleA[i][j] == 0:
                    x = j
                    y = i
        return x, y

    def isTheAnswer(self, puzzleA):
        if self.calculateH(puzzleA) == 0:
            return True
        return False

    def findPath(self, actualPuzzle, x, y):
        while True:
            options = []
            if self.isTheAnswer(actualPuzzle.puzzle):
                print('Solución Encontrada')
                break
            print("---- Options ----")
            for v in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xn = x + v[0]
                yn = y + v[1]
                if xn < 0 or xn > 2 or yn < 0 or yn > 2 or (xn == actualPuzzle.x and yn == actualPuzzle.y):
                    continue
                newPuzzle = copy.deepcopy(actualPuzzle)
                aux = newPuzzle.puzzle[y][x]
                newPuzzle.puzzle[y][x] = newPuzzle.puzzle[yn][xn]
                newPuzzle.puzzle[yn][xn] = aux
                options.append(Option(newPuzzle.puzzle, self.calculateH(newPuzzle.puzzle), x, y, xn, yn))
                print("H:", self.calculateH(newPuzzle.puzzle))
                for i in range(3):
                    print(list(newPuzzle.puzzle[i]))
            print("--------------------")
            actualPuzzle = min(options, key=lambda x: x.h)
            x = actualPuzzle.xn
            y = actualPuzzle.yn
            print('Selected Option')
            for i in range(3):
                print(list(actualPuzzle.puzzle[i]))
            print('\n')

puzzle = [[1, 2, 3],
          [8, 0, 4],
          [7, 6, 5]]

puzzleGame = [[2, 8, 3],
              [1, 6, 4],
              [7, 0, 5]]


hill_climb = HillClimb()
x, y = hill_climb.setStartNode(puzzleGame)
print(x, y)
actualPuzzle = Option(puzzleGame, hill_climb.calculateH(puzzleGame), x, y, x, y)
hill_climb.findPath(actualPuzzle, x, y)