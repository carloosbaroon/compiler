from enum import Enum

class TokenType(Enum):
    ID = 101
    NUM = 111
    ELSE = 'else'
    IF = 'if'
    INT = 'integer'
    FOR = 'for'
    WHILE = 'while'
    RETURN = 'return'
    VOID = 'void'
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    OVER = '/'
    LT = '<'
    LTE = '<='
    GT = '>'
    GTE = '>='
    EQUALS = '=='
    DIFFERENT = '!='
    ASSIGN = '='
    SEMI = ';'
    COMMA = ','
    LPAREN = '('
    RPAREN = ')'
    LSQUAREP = '['
    RSQUAREP = ']'
    LKPAREN = '{'
    RKPAREN = '}'
    OPENCOMMENT = '/*'
    CLOSECOMMENT = '*/'
    COMMENT = 123
    ENDFILE = '$'

class ReservedWords(Enum):
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    FOR = 'for'
    WHILE = 'while'
    RETURN = 'return'
    VOID = 'void'

#***********   Syntax tree for parsing ************

class NodeKind(Enum):
    StmtK = 0
    ExpK = 1

class StmtKind(Enum):
    IfK = 0
    WhileK = 1
    ForK = 2
    ReturnK = 3
    AssignK = 4
    FunctK = 5

class ExpKind(Enum):
    OpK = 0
    ConstK = 1
    IdK = 2

# ExpType is used for type checking
class ExpType(Enum):
    Void = 0
    Integer = 1

# Máximo número de hijos por nodo (3 para el if)
MAXCHILDREN = 3

class TreeNode:
    def __init__(self):
        # MAXCHILDREN = 3 está en globalTypes
        self.child = [None] * MAXCHILDREN # tipo treeNode
        self.sibling = None               # tipo treeNode
        self.lineno = 0                   # tipo int
        self.nodekind = None              # tipo NodeKind, en globalTypes
        # en realidad los dos siguientes deberían ser uno solo (kind)
        # siendo la  union { StmtKind stmt; ExpKind exp;}
        self.stmt = None                  # tipo StmtKind
        self.exp = None                   # tipo ExpKind
        # en realidad los tres siguientes deberían ser uno solo (attr)
        # siendo la  union { TokenType op; int val; char * name;}
        self.op = None                    # tipo TokenType
        self.val = None                   # tipo int
        self.name = None                  # tipo String
        # for type checking of exps
        self.type = None                  # de tipo ExpType