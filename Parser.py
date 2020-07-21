from enum import Enum
from globalTypes import *
from lexer import *
# Impresion de arbol basado en ParserTyny.py
token_g = ''
currenttoken_g = ''
position_g = ''
endentacion = ''
lastTruePosition_g = ''
band = True
SintaxTree = None
error = False
lineno = 1
iniCToken = ""
iniToken = ""
iniPos = 0
# Function newStmtNode creates a new statement
# node for syntax tree construction
def newStmtNode(kind):
    t = TreeNode();
    if (t==None):
        print("Out of memory error at line " + lineno)
    else:
        #for i in range(MAXCHILDREN):
        #    t.child[i] = None
        #t.sibling = None
        t.nodekind = NodeKind.StmtK
        t.cuerpo = kind
        t.lineno = lineno
    return t

# Function newExpNode creates a new expression
# node for syntax tree construction

def newExpNode(kind):
    t = TreeNode()
    if (t==None):
        print("Out of memory error at line " + lineno)
    else:
        # for i in range(MAXCHILDREN):
        #    t.child[i] = None
        # t.sibling = None
        t.nodekind = NodeKind.ExpK
        t.exp = kind
        t.lineno = lineno
        t.type = ExpType.Void
    return t

# Procedure printToken prints a token
# and its lexeme to the listing file
def printToken(token, tokenString):
    if token in {TokenType.ELSE, TokenType.IF, TokenType.INT, TokenType.FOR,
                 TokenType.WHILE, TokenType.RETURN, TokenType.VOID}:
      print(" reserved word: " + tokenString);
    elif token == TokenType.ASSIGN:
        print("==")
    elif token == TokenType.LT:
        print("<")
    elif token == TokenType.EQUALS:
        print("=")
    elif token == TokenType.LPAREN:
        # print(listing,"(")
        print("(")
    elif token == TokenType.RPAREN:
        print(")")
    elif token == TokenType.LSQUAREP:
        # print(listing,"(")
        print("[")
    elif token == TokenType.RSQUAREP:
        print("]")
    elif token == TokenType.SEMI:
        print(";")
    elif token == TokenType.PLUS:
        print("+")
    elif token == TokenType.MINUS:
        print("-")
    elif token == TokenType.TIMES:
        print("*")
    elif token == TokenType.OVER:
        print("/")
    elif token == TokenType.ENDFILE:
        print("$")
    elif token == TokenType.NUM:
      print("NUM, val= " + tokenString)
    elif token == "ID":
        print("ID, name= " + tokenString);
    else: # should never happen
        print("Unknown token: " + str(token))

# Variable indentno is used by printTree to
# store current number of spaces to indent
indentno = 0

# printSpaces indents by printing spaces */
def printSpaces():
    print(" "*indentno, end = "")

# procedure printTree prints a syntax tree to the
# listing file using indentation to indicate subtrees
def printTree(tree):
    global indentno
    indentno+=2 # INDENT
    while tree != None:
        printSpaces();
        if (tree.nodekind==NodeKind.StmtK):
            if tree.cuerpo == StmtKind.IfK:
                print(tree.lineno, "If")
            elif tree.cuerpo == StmtKind.RepeatK:
                print(tree.lineno, "Repeat")
            elif tree.cuerpo == StmtKind.AssignK:
                print(tree.lineno, "Assign to: ",tree.name)
            elif tree.cuerpo == StmtKind.ReadK:
                print(tree.lineno, "Read: ",tree.name)
            elif tree.cuerpo == StmtKind.WriteK:
                print(tree.lineno, "Write")
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        elif tree.nodekind==NodeKind.ExpK:
            if tree.exp == ExpKind.OpK:
                print(tree.lineno, "Op: ", end ="")
                printToken(tree.op," ")
            elif tree.exp == ExpKind.ConstK:
                print(tree.lineno, "Const: ",tree.val)
            elif tree.exp == ExpKind.IdK:
                print(tree.lineno, "Id: ",tree.name)
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        else:
            print(tree.lineno, "Unknown node kind");
        for i in range(MAXCHILDREN):
            printTree(tree.child[i])
        tree = tree.sibling
    indentno-=2 #UNINDENT

# the primary function of the parser
# Function parse returns the newly
# constructed syntax tree

def updateToken(ctoken, token, pos):
    global currenttoken_g
    global token_g
    global position_g
    global lastTruePosition_g
    global band
    currenttoken_g = ctoken
    token_g = token
    position_g = pos

def errorSintaxis(mensaje):
    global position_g
    global token_g
    rposition = position_g
    if token_g != '$':
        print('Error de sintaxis ' + mensaje)
    else:
        print('' + mensaje)

def match():
    global currenttoken_g, token_g
    currentToken, token, contador = getToken()
    updateToken(currentToken, token, contador)
    updatePos(contador)
    if currenttoken_g == TokenType.COMMENT:
        match()

def UpdateLastToken(ct, t, p):
    global currenttoken_g
    global token_g
    global position_g
    currenttoken_g = ct
    token_g = t
    position_g = p
    updatePos((p+(len(t))))

def updateInitialPos(band, msg):
    global currenttoken_g
    global token_g
    global position_g
    global iniCToken
    global iniToken
    global iniPos
    if band:
        iniCToken = currenttoken_g
        iniToken = token_g
        iniPos = position_g - len(token_g)

def programa():
    global band
    global iniCToken
    global iniToken
    global iniPos
    global token_g
    global currenttoken_g
    global position_g
    banderaFunc = False
    banderaFinal = False
    t = None
    p = None
    p = t
    while token_g != '$':
        if not banderaFunc:
           updateInitialPos(banderaFinal, "")
           banderaFinal, t = declarar()
        if not banderaFinal or banderaFunc:
            UpdateLastToken(iniCToken, iniToken, iniPos)
            banderaFinal, t = funcion()
            iniCToken = currenttoken_g
            iniToken = token_g
            iniPos = position_g
            if not banderaFinal:
                banderaFunc = True
        if banderaFinal:
            printTree(t)
    return t

def declarar():
    global token_g
    global currenttoken_g
    global band
    t = None
    p = None
    band = False
    if token_g == 'int':
        t = newExpNode(ExpKind.ConstK)
        t.val = token_g
        match()
        band, p = declaracion()
        t.child[0] = p
        if token_g != '(' and band:
            band = True
            while token_g == ',':
                match()
                band, q = declaracion()
            p.child[0] = q
        elif token_g == '(':
            match()
            band, a = parametros()
            p.child[1] = a
            if token_g == ')' and band:
                band = True
                match()
                while token_g == ',':
                    match()
                    if currenttoken_g == 'ID':
                        band = False
                        match()
                        if token_g == '(':
                            match()
                            band, t = parametros()
                            if token_g == ')' and band:
                                match()
                                band = False
                            else:
                                errorSintaxis("Falta ')'")
                                band = False
                        else:
                            errorSintaxis("Falta'('")
            else:
                errorSintaxis("Falta')'")
                band = True
                match()
    if token_g == ';':
        match()
        band = True
    else:
        band = False
    return band, t

def declaracion():
    global token_g
    global currenttoken_g
    global band
    t = None
    band = False
    if currenttoken_g == 'ID':
        band = True
        t = newExpNode(ExpKind.IdK)
        t.name = token_g
        if (t!=None):
          t.op = token_g
        match()
        if token_g == '[':
            match()
            band = False
            if currenttoken_g == TokenType.NUM:
                p = newExpNode(ExpKind.ConstK)
                p.val = int
                if (p != None):
                    p.child[0] = t
                    p.op = token_g
                    t = p
                match()
                if token_g == ']':
                    match()
                    band = True
    return band, t

def parametros():
    global token_g
    global currenttoken_g
    global band
    t = None
    band = False
    if token_g == 'void':
        t = newExpNode(ExpKind.ConstK)
        t.val = token_g
        match()
        band = True
    elif token_g == 'int':
        t = newExpNode(ExpKind.ConstK)
        t.val = token_g
        band = False
        match()
        if currenttoken_g == 'ID':
            p = newExpNode(ExpKind.IdK)
            p.name = token_g
            t.child[0] = p
            match()
            band = True
            if token_g == '[':
                match()
                band = False
                if token_g == ']':
                    match()
                    band = True
            if token_g == ',':
                while token_g == ',' and band:
                    match()
                    band = False
                    if token_g == 'int':
                        q = newExpNode(ExpKind.ConstK)
                        q.val = token_g
                        match()
                        band = False
                        if currenttoken_g == 'ID':
                            l = newExpNode(ExpKind.IdK)
                            l.name = token_g
                            q.child[0] = l
                            t.sibling = q
                            match()
                            band = True
                            if token_g == '[':
                                match()
                                band = False
                                if token_g == ']':
                                    match()
                                    band = True
                    else:
                        errorSintaxis("Falta 'int'")
                        band = True
                        match()
    return band, t

def funcion():
    global currenttoken_g
    global token_g
    global position_g
    global band
    contador =0
    band = False
    t = None
    c = None
    if token_g == 'int' or 'void':
        t = newExpNode(ExpKind.ConstK)
        t.val = token_g
        match()
        if currenttoken_g == 'ID':
            q = newExpNode(ExpKind.IdK)
            q.name = token_g
            t.child[0] = q
            match()
            if token_g == '(':
                match()
                band, l = parametros()
                q.child[0] = l
                if token_g == ')' and band:
                    match()
                    if token_g == '{':
                        band = True
                        match()
                        if token_g == 'int':
                            while token_g == 'int':
                                m = newExpNode(ExpKind.ConstK)
                                m.val = token_g
                                match()
                                band, n = declaracion()
                                if token_g == ',' and band:
                                    while token_g == ',':
                                        match()
                                        band, c = declaracion()
                                        n.sibling = c
                                if token_g == ';' and band:

                                    m.child[0] = n
                                    match()
                                    band = True
                                else:
                                    errorSintaxis(" Falta ';'")
                                    band = False
                                q.child[1] = m
                        if token_g != '}':
                            cont = 0
                            while band and token_g != '}':
                                band, a = cuerpo()
                                if contador == 0:
                                    temp = a
                                else:
                                    temp.sibling = a
                                    temp = a
                                cont += 1
                            q.child[1] = temp
                            band2 = 0
                        if token_g == '}' and band:
                            band = True
                            match()
    return band, t

def cuerpo():
    global token_g
    global currenttoken_g

    t = None
    band = False
    if token_g == 'if':
        t = newStmtNode(StmtKind.IfK)
        t.op = TokenType.IF
        match()
        if token_g == '(':
            match()
            band, t.child[0] = expr()
            if token_g == ')' and band:
                match()
                band, t.child[1] = cuerpo()
                if token_g == 'else' and band:
                    j = newExpNode(ExpKind.IdK)
                    j.name = token_g
                    t.sibling = j
                    match()
                    band, f = cuerpo()
                    j.child[0] = f
    if token_g == 'while':
        t = newStmtNode(StmtKind.WhileK)
        t.op = TokenType.IF
        match()
        if token_g == '(':
            match()
            band, t = expr()

            if token_g == ')' and band:
                band, t = cuerpo()
            else:
                errorSintaxis(" Falta ')'")
    if token_g == 'return':
        t = newExpNode(ExpKind.IdK)
        t.name = token_g
        match()
        band = True
        if token_g != ';':
            band, t = expr()
        if token_g == ';' and band:
            match()
    if currenttoken_g == 'ID':
        t = newExpNode(ExpKind.IdK)
        t.name = token_g
        match()
        band = False
        if token_g == '(':
            match()
            if token_g != ')':
                band, l = expr()
                t.child[0] = l
                while token_g == ',' and band:
                    match()
                    band, m = expr()
                    t.child[1] = m
            if token_g == ')':
                match()
                if token_g == ';' and band:
                    match()
                    band = True
        elif token_g == '[' or token_g == '=':
            band, o = asignacion()
            t.child[0] = o
    if token_g == '{':
        match()
        band, t = cuerpo()
        if token_g == '}' and band:
            match()
            band = True
    if token_g == ';':
        match()
        band = True
    return band, t

def asignacion():
    global token_g
    global currenttoken_g
    global band

    band = False
    if token_g == '[':
        match()
        band, t = expr()
        if token_g == ']' and band:
            match()
            band = True
        else:
            errorSintaxis("Falta']'")
    elif token_g == '=':
        t = newExpNode(ExpKind.IdK)
        t.name = "="
        match()
        band, z = expr()
        t.sibling = z
    return band, t

def expr():
    global token_g
    global currenttoken_g
    global band

    band = False
    t = None
    if token_g == '-':
        t = newExpNode(ExpKind.OpK)
        t.op = token_g
        match()
        band, t = expr()
    elif token_g == '!':
        t = newExpNode(ExpKind.OpK)
        t.op = token_g
        match()
        band, t = expr()
    elif currenttoken_g == 'ID' or currenttoken_g == TokenType.NUM:
        if currenttoken_g == 'ID':
            t = newExpNode(ExpKind.IdK)
            t.name = token_g
        else:
            t = newExpNode(ExpKind.ConstK)
            t.val = int(token_g)
        match()
        band = True
        if token_g in '+-*/':
            t = newExpNode(ExpKind.OpK)
            t.op = token_g
            match()
            band, t = expr()
        elif token_g == '==' or token_g == '!=' or token_g == '<=' or token_g == '<' or token_g == '>=' or token_g == '>':
            l = newExpNode(ExpKind.OpK)
            l.op = token_g
            t.child[0] = l
            match()
            band, t.child[1] = expr()
        elif token_g == '(':
            match()
            band = True
            if token_g != ')':
                if token_g == '-' or token_g == '!' or currenttoken_g == 'ID' or currenttoken_g == TokenType.NUM or token_g == '(':
                    if currenttoken_g == 'ID':
                        z = newExpNode(ExpKind.OpK)
                        z.op = token_g
                        t.child[1] = z
                    elif currenttoken_g == TokenType.NUM:
                        a = newExpNode(ExpKind.ConstK)
                        a.val = int(token_g)
                        t.child[0] = a
                    elif token_g != '(':
                        b= newExpNode(ExpKind.OpK)
                        b.op = token_g
                    band, p = expr()
                    if band:
                        t.child[0] = p
                    while token_g == ',' and band:
                        match()
                        band, t = expr()
            if token_g == ')' and band:
                match()
                band = True
            else:
                errorSintaxis(" Falta')'")
        elif token_g == '[':
            match()
            band, t = expr()
            if token_g == ']' and band:
                match()
                band = True
            else:
                errorSintaxis(" Falta']'")

    elif token_g == '(':
        match()
        band, t = expr()
        if token_g == ')' and band:
            match()
            band = True
        else:
            errorSintaxis(" Falta')'")
    elif currenttoken_g == TokenType.NUM:
        t = newExpNode(ExpKind.ConstK)
        t.val = int(token_g)
        match()
        band = True
    elif token_g == '+' or token_g == '*' or token_g == '/':
        t = newExpNode(ExpKind.OpK)
        t.op = token_g
        match()
        band, t = expr()
    elif token_g == '==' or token_g == '!=' or token_g == '<=' or token_g == '<' or token_g == '>=' or token_g == '>':
        t = newExpNode(ExpKind.OpK)
        t.op = token_g
        match()
        band, t = expr()
    return band, t

def parser(imprese = True):
    global currenttoken_g
    global token_g
    currentToken, token, contador = getToken()
    updatePos(contador)
    if currentToken == TokenType.COMMENT:
        match()
    else:
        updateToken(currentToken, token, contador)
    t = programa()
    endentacion = 0
    if token_g != '$':
        errorSintaxis('Termina leer antes de acabar archivo')
    else:
        errorSintaxis('Archivo leido con exito')
        # printTree(t)