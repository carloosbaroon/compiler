from globalTypes import *

def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long

with open('matrizAL.txt', 'r') as f:
    fil, col = [int(x) for x in next(f).split()]
    simbolos = next(f).split('.')
    M = [[int(x) for x in line.split()] for line in f]
    
#print(fil, col)
#print(simbolos)
#print(M)

mapa = {}
for i in range(len(simbolos)):
    for c in simbolos[i]:
        mapa[c] = i

def reservedLookup(tokenString):
    for w in ReservedWords:
        if tokenString == w.value:
            tokenString = "Reserved Word"
            return tokenString
    tokenString = "ID"
    return tokenString
    


def getToken(imprime = True):
    tokenString = ""
    currentToken = None
    estado = 0                  # estado inicial
    token = ''
    contador = 0
    position = 0
    commentFlag = ''
    #print(contador, progLong)
    while contador < progLong:
        try:
            c = programa[contador]
            estado = M[estado][mapa[c]]
            #print(c)
            #print(estado)
            if estado == 1:
                token += c
                tokenString = token
                currentToken = TokenType.PLUS
                print("PLUS", "=",tokenString)
                token = ''
                estado = 0
            if estado == 2:
                token += c
                tokenString = token
                currentToken = TokenType.MINUS
                print("MINUS", "=",tokenString)
                token = ''
                estado = 0
            if estado == 3:
                token += c
                tokenString = token
                currentToken = TokenType.TIMES
                print("TIMES", "=",tokenString)
                token = ''
                estado = 0
            if estado == 4:
                token += c
                if programa[contador + 1] == '*':
                    estado = 6
                else:
                    tokenString = token
                    currentToken = TokenType.OVER
                    print("OVER", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 6:
                contador += 1
                c = programa[contador]
                token += c
                estado = 7
            if estado == 7:
                while commentFlag != '*/':
                    if c == '*' and programa[contador + 1] == '/':
                        commentFlag == '*/'
                        contador += 1
                        c = programa[contador]
                        token += c
                        break
                    contador += 1
                    c = programa[contador]
                    token += c
                tokenString = token
                currentToken = TokenType.COMMENT
                print("COMMENT", "=",tokenString)
                token = ''
                estado = 0
            if estado == 10:
                token += c
                if programa[contador + 1] == '=':
                    estado = 12
                else:
                    tokenString = token
                    currentToken = TokenType.LT
                    print("LESS THAN", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 12:
                contador += 1
                c = programa[contador]
                token += c
                tokenString = token
                currentToken = TokenType.LTE
                print("LESS OR EQUAL", "=",tokenString)
                token = ''
                estado = 0
            if estado == 13:
                token += c
                if programa[contador + 1] == '=':
                    estado = 15
                else:
                    tokenString = token
                    currentToken = TokenType.GT
                    print("GREATER THAN", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 15:
                contador += 1
                c = programa[contador]
                token += c
                tokenString = token
                currentToken = TokenType.GTE
                print("GREATER OR EQUAL", "=",tokenString)
                token = ''
                estado = 0
            if estado == 16:
                token += c
                if programa[contador + 1] == '=':
                    estado = 18
                else:
                    tokenString = token
                    currentToken = TokenType.ASSIGN
                    print("ASSIGN", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 18:
                contador += 1
                c = programa[contador]
                token += c
                tokenString = token
                currentToken = TokenType.EQUALS
                print("EQUALS", "=",tokenString)
                token = ''
                estado = 0
            if estado == 19:
                token += c
            if estado == 20:
                token += c
                tokenString = token
                currentToken = TokenType.DIFFERENT
                print("DIFFERENT", "=",tokenString)
                token = ''
                estado = 0
            if estado == 21:
                token += c
                tokenString = token
                currentToken = TokenType.SEMI
                print("SEMICOLON", "=",tokenString)
                token = ''
                estado = 0
            if estado == 22:
                token += c
                tokenString = token
                currentToken = TokenType.COMMA
                print("COMMA", "=",tokenString)
                token = ''
                estado = 0
            if estado == 23:
                token += c
                tokenString = token
                currentToken = TokenType.LPAREN
                print("LPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 24:
                token += c
                tokenString = token
                currentToken = TokenType.RPAREN
                print("RPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 25:
                token += c
                tokenString = token
                currentToken = TokenType.LSQUAREP
                print("LSPARENP", "=",tokenString)
                token = ''
                estado = 0
            if estado == 26:
                token += c
                tokenString = token
                currentToken = TokenType.RSQUAREP
                print("RPARENP", "=",tokenString)
                token = ''
                estado = 0
            if estado == 27:
                token += c
                tokenString = token
                currentToken = TokenType.LKPAREN
                print("LKPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 28:
                token += c
                tokenString = token
                currentToken = TokenType.RKPAREN
                print("RKPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 29:
                token += c
            if estado == 30:
                currentToken = reservedLookup(token)
                tokenString = token
                print(currentToken, "=",tokenString)
                token = ''
                estado = 0
            if estado == 31:
                token += c
            if estado == 32:
                currentToken = TokenType.NUM
                tokenString = token
                print("NUM" ,"=", tokenString)
                token = ''
                estado = 0
            if estado == 33:
                token += c
                tokenString = token
                currentToken = TokenType.ERROR
                print("Error al declarar ID", tokenString)
                position = len(token)
                print(" "*(position+19),"^")
                token = ''
                estado = 0
            if estado == 34:
                token += c
                tokenString = token
                currentToken = TokenType.ERROR
                print("Error al declarar NUM", tokenString)
                position = len(token)
                print(" "*(position+20),"^")
                token = ''
                estado = 0
            if estado == 35:
                tokenString = token
                currentToken = reservedLookup(token)
                print(currentToken, "=",tokenString)
                token = ''
                estado = 0
                contador -= 1
            if estado == 36:
                tokenString = token
                currentToken = TokenType.NUM
                print("NUM" ,"=", token)
                token = ''
                estado = 0
                contador -= 1        
            contador += 1
        except:
            token += c
            tokenString = token
            currentToken = TokenType.ERROR
            print("Caracter no definido", "=",tokenString)
            contador += 1
            token = ''
        if (contador == progLong):
                token = TokenType.ENDFILE
    return token, token