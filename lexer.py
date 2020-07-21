from globalTypes import *
positionG = 0

def updatePos(pos):
    global positionG
    positionG = pos

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
    line = 1
    contador = positionG
    position = 0
    commentFlag = ''
    #print(contador, progLong)
    while contador < progLong+1:
        try:
            c = programa[contador]
            estado = M[estado][mapa[c]]
            #print(c)
            #print(estado)
            if estado == 1:
                token += c
                tokenString = token
                currentToken = TokenType.PLUS
                contador += 1
                return currentToken, tokenString, contador
                print("PLUS", "=",tokenString)
                token = ''
                estado = 0
            if estado == 2:
                token += c
                tokenString = token
                currentToken = TokenType.MINUS
                contador += 1
                return currentToken, tokenString, contador
                print("MINUS", "=",tokenString)
                token = ''
                estado = 0
            if estado == 3:
                token += c
                tokenString = token
                currentToken = TokenType.TIMES
                contador += 1
                return currentToken, tokenString, contador
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
                    contador += 1
                    return currentToken, tokenString, contador
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
                contador += 1
                return currentToken, tokenString, contador
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
                    contador += 1
                    return currentToken, tokenString, contador
                    print("LESS THAN", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 12:
                contador += 1
                c = programa[contador]
                token += c
                tokenString = token
                currentToken = TokenType.LTE
                contador += 1
                return currentToken, tokenString, contador
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
                    contador += 1
                    return currentToken, tokenString, contador
                    print("GREATER THAN", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 15:
                contador += 1
                c = programa[contador]
                token += c
                tokenString = token
                currentToken = TokenType.GTE
                contador += 1
                return currentToken, tokenString, contador
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
                    contador += 1
                    return currentToken, tokenString, contador
                    print("ASSIGN", "=",tokenString)
                    token = ''
                    estado = 0
            if estado == 18:
                contador += 1
                c = programa[contador]
                token += c
                tokenString = token
                currentToken = TokenType.EQUALS
                contador += 1
                return currentToken, tokenString, contador
                print("EQUALS", "=",tokenString)
                token = ''
                estado = 0
            if estado == 19:
                token += c
            if estado == 20:
                token += c
                tokenString = token
                currentToken = TokenType.DIFFERENT
                contador += 1
                return currentToken, tokenString, contador
                print("DIFFERENT", "=",tokenString)
                token = ''
                estado = 0
            if estado == 21:
                token += c
                tokenString = token
                currentToken = TokenType.SEMI
                contador += 1
                return currentToken, tokenString, contador
                print("SEMICOLON", "=",tokenString)
                token = ''
                estado = 0
            if estado == 22:
                token += c
                tokenString = token
                currentToken = TokenType.COMMA
                contador += 1
                return currentToken, tokenString, contador
                print("COMMA", "=",tokenString)
                token = ''
                estado = 0
            if estado == 23:
                token += c
                tokenString = token
                currentToken = TokenType.LPAREN
                contador += 1
                return currentToken, tokenString, contador
                print("LPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 24:
                token += c
                tokenString = token
                currentToken = TokenType.RPAREN
                contador += 1
                return currentToken, tokenString, contador
                print("RPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 25:
                token += c
                tokenString = token
                currentToken = TokenType.LSQUAREP
                contador += 1
                return currentToken, tokenString, contador
                print("LSPARENP", "=",tokenString)
                token = ''
                estado = 0
            if estado == 26:
                token += c
                tokenString = token
                currentToken = TokenType.RSQUAREP
                contador += 1
                return currentToken, tokenString, contador
                print("RPARENP", "=",tokenString)
                token = ''
                estado = 0
            if estado == 27:
                token += c
                tokenString = token
                currentToken = TokenType.LKPAREN
                contador += 1
                return currentToken, tokenString, contador
                print("LKPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 28:
                token += c
                tokenString = token
                currentToken = TokenType.RKPAREN
                contador += 1
                return currentToken, tokenString, contador
                print("RKPAREN", "=",tokenString)
                token = ''
                estado = 0
            if estado == 29:
                token += c
            if estado == 30:
                currentToken = reservedLookup(token)
                tokenString = token
                #contador += 1
                return currentToken, tokenString, contador
                print(currentToken, "=",tokenString)
                token = ''
                estado = 0
            if estado == 31:
                token += c
            if estado == 32:
                currentToken = TokenType.NUM
                tokenString = token
                #contador += 1
                return currentToken, tokenString, contador
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
                #contador += 1
                return currentToken, tokenString, contador
                print(currentToken, "=",tokenString)
                token = ''
                estado = 0
                contador -= 1
            if estado == 36:
                tokenString = token
                currentToken = TokenType.NUM
                #contador += 1
                return currentToken, tokenString, contador
                print("NUM" ,"=", token)
                token = ''
                estado = 0
                contador -= 1        
            contador += 1
            #return currentToken, tokenString, contador
        except:
            token += c
            tokenString = token
            #currentToken = TokenType.ERROR
            print("Caracter no definido", "=",tokenString)
            contador += 1
            token = ''

        if c == '\n':
            line += 1
        if (c == '$'):
                currentToken = TokenType.ENDFILE
                tokenString = TokenType.ENDFILE.value
                return currentToken, tokenString, contador
    return currentToken, tokenString, contador
