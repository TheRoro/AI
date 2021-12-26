import nltk
from nltk import CFG
from nltk.parse.generate import generate
gramatica = CFG.fromstring("""
S -> OR CON OR
OR -> SV | SV SN SV
SV -> AD V | PR V AD | AD V SN SP
SN -> AD | PD| AR NC
SP -> PR NC
AD -> 'no' | 'siempre' | 'simplemente' | 'más' | 'menos'
AR -> 'un' | 'muchos' | 'todos' | 'otros' | 'distintos'
NC -> 'años' | 'tipos' | 'saberes' | 'elecciones'
V -> 'existe' | 'saber' | 'dar' | 'existen' | 'trabajar'
PR -> 'de'
CON -> '.'|','
PD -> 'éste' | 'eso' | 'aquellas'
""")
print('La gramática: ', gramatica)

s = "no existe eso de saber menos . simplemente existen distintos tipos de saberes"
s = s.split()
try:
    gramatica.check_coverage(s)
    print('Esta correctamente escrito')
except:
    print('La frase no esta en la gramática')

parser = nltk.ChartParser(gramatica)
for arbol in parser.parse(s):
    print(arbol)
