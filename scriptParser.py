from globalTypes import *
from Parser import *
f = open('gcdTest.c-', 'r')
programa = f.read()
progLong = len(programa)
programa = programa + '$'
posicion = 0
globales(programa, posicion, progLong)
AST = parser(True)