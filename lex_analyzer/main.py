# A01411195   Soraya Lizeth Maqueda Gutiérrez
# Lenguajes y Traductores - Analizador de Léxico

# Ply tools to create lexic analyzer
from colorama import Fore
import numpy as np
import sys
import re

# Token Definitions
# Tokens: Operators, Reserved Words, Id's for grammar rules

# For reserved words, we establish a rule that matches with the id so that 
# we can search for the function that matches it.

reserved = {
    'array' : 'ARRAY',
    'begin' : 'BEGIN',
    'digit' : 'FLOAT',
    'else' : 'ELSE',
    'elsif': 'ELSIF',
    'end' : 'END',
    'for' : 'FOR',
    'if' : 'IF',
    'in' : 'IN',
    'integer' : 'INT',
    'is' : 'IS',
    'loop' : 'LOOP',
    'procedure' : 'PROCEDURE',
    'range' : 'RANGE',
    'type' : 'TYPE',
    'use' : 'USE',
    'with' : 'WITH',
    'while' : 'WHILE',
    'then' : 'THEN',
    'and' : 'AND',
    'or' : 'OR'
}

tokens = [
    'ID', 
    'FLOATNUM',
    'NUMBER',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'TIMES',
    'GT',
    'GTE',
    'LT',
    'LTE',
    'EQUAL',
    'SEMICOLON',
    'SUSPENSIVE',
    'COMMA',
    'BRAOPEN',
    'BRACLOSE',
    'NEWLINE',
    'TAB'
] + list(reserved.values())

# Aritmetic Operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'/'
t_LTE = r'<\|='
t_GTE = r'>\|='
t_EQUAL = r'\|='
t_TIMES = r'\*'
t_GT = r'>'
t_LT = r'<'

# Special Tokens
t_SEMICOLON = r'\;'
t_ASSIGN = r'\:='
t_SUSPENSIVE = r'\.\.\.'
t_COMMA = r','
t_BRAOPEN = r'\('
t_BRACLOSE = r'\)'

# Token to ignore
t_ignore = r'   \t'
 
# Precedence 
# By default, there's an ambiguety as to the expression syntax, therefore yacc allows
# us to set a precedence an associate it to individaul tags.
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# Dictionary for Variable Names
names = [] # Symbol Table
tempSymb =[] # Temporary to append until len == 4
tempId = '' # To determine unfinished var declaration

# Operands
operands = []
values = []

# Operators
operators = []
operatorsHelper = ('PLUS' , 'MINUS' , 'DIVIDE' , 'LTE' , 'LT' , 'GTE' , 'GT' , 'TIMES' , 'ASSIGN')

# Loops Translation
loops = [] # Stack for generated code
jumps = [] # Jump Stack
whileDirs = [] # Stack to return to while if true
loopsHelper = ('IF' , 'OR' , 'ELSE' , 'ELIF' , 'END' , 'FOR' , 'LOOP' , 'WHILE')
loopCnt = 0

# Quadruples
quad = []

# Error Count
err = []

# Token Count
parsedTokens = []

# Output Files
errorLog = open('ErrorLogs.txt', mode='w')
tokenLog = open('TokenLog.txt', mode='w')
SymbolTable = open('SymbolTable.txt', mode='w')
Quadruples = open('Quadruples.txt', mode='w')

# Token Functions
# Regex definition in functions. This implemenation is useful because
# it allows us to manipulate the value of the token received.

# Variable Id
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    if t.value not in tokens and not KeyError: names[t.value]
    print(Fore.LIGHTGREEN_EX + '\nID: ' + t.value)
    
    return t

# type
def t_TYPE(t):
    r'type'
    t.type = reserved.get(t.value, 'TYPE')
    print(Fore.LIGHTGREEN_EX + 'Variable type being identified...')
    return t

# is
def t_IS(t):
    r'is'
    t.type = reserved.get(t.value, 'IS')
    print(Fore.LIGHTGREEN_EX + '\nis of type...')
    return t

# Integers
def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(Fore.RED + 'Value too large %d', t.value)
        err.append({'Value Error': 'Float value too large at line ' + str(t.lineno)})
    
    print(Fore.LIGHTGREEN_EX + '\nInteger of value: ' + str(t.value))
    return t

# Floats
def t_FLOAT(t):
    r'[+-]?([0-9]*[.])?[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(Fore.RED + 'Value too large %d', t.value)
        err.append({'Value Error' : 'Integer Value too large at line ' + str(t.lineno)})
        t.value = 0
    
    print(Fore.LIGHTGREEN_EX + '\nFloat of value: ' + str(t.value))
    return t

# use
def t_USE(t):
    r'use'
    t.type = reserved.get(t.value, 'USE')
    print(Fore.CYAN + '\nNew Context declared...')
    return t

# procedure
def t_PROCEDURE(t):
    r'procedure'
    t.type = reserved.get(t.value, 'PROCEDURE')
    print(Fore.CYAN + '\nProcedure delcared...')
    return t

# Characters to ignore
# t_ prefix for python's native library to identify a token as a regex

# Tab
def t_TAB(t):
    r' \t'
    t.lexer.lineno += t.value.count('\t')
    print(Fore.CYAN + '\nSkipped tab...')
    pass

# New Line
def t_NEWLINE(t):
    r' \n'
    t.lexer.lineno += t.value.count('\n')
    print(Fore.CYAN + '\nSkipped new line...')
    pass

# Comment
def t_comment(t):
    r'\--'
    pass

# Error Handling
def t_error(t):
    print(Fore.RED + 'Illegal character %s' % t.value[0] + t.type)
    err.append({'Token Error': 'Illegal char at line ' + str(t.lineno)})
    t.lexer.skip(1)

# Building the lexer
import ply.lex as lex
lexer = lex.lex()

# Syntax Rules

# Array
def t_ARRAY(t):
    r'array'
    t.type = 'ARRAY'
    print(Fore.CYAN + '\nArray declared...')
    return t

# begin
def t_BEGIN(t):
    r'begin'
    t.type = reserved.get(t.value, 'BEGIN')
    print(Fore.CYAN + '\nBegin procedure')
    return t

# else
def t_ELSE(t):
    r'else'
    t.type = reserved.get(t.value, 'ELSE')
    return t

# elsif
def t_ELSIF(t):
    r'elsif'
    t.type = reserved.get(t.value, 'ELSIF')
    return t

# end
def t_END(t):
    r'end'
    t.type = reserved.get(t.value, 'END')
    return t

# for
def t_FOR(t):
    r'for'
    t.type = reserved.get(t.value, 'FOR')
    return t

# if
def t_IF(t):
    r'if'
    t.type = reserved.get(t.value, 'IF')
    return t

# and
def t_AND(t):
    r'and'
    t.type = reserved.get(t.value, 'AND')
    return t

# or
def t_OR(t):
    r'or'
    t.type = reserved.get(t.value, 'OR')
    return t

# in
def t_IN(t):
    r'in'
    t.type = reserved.get(t.value, 'IN')
    return t

# loop
def t_LOOP(t):
    r'loop'
    t.type = reserved.get(t.value, 'LOOP')
    return t


# range
# def t_RANGE(t):
#     isRangeRegex = '(\(+[0-9]+\.\.\.[0-9]+)+\,*([0-9]+\.\.\.[0-9]+)*\,*([0-9]+\.\.\.[0-9]+\)+)*'
#     ranges = re.search(isRangeRegex, t).group() # A string with the ranges is returned. 
#                                                 # Example: (0...4) or (0...4,0...5) or (0...4,0...2,0...5)
#     t.type = 'RANGE'
#     return t, ranges

# with
def t_WITH(t):
    r'with'
    t.type = reserved.get(t.value, 'WITH')
    return t

# while
def t_WHILE(t):
    r'while'
    t.type = reserved.get(t.value, 'WHILE')
    return t

# then
def t_THEN(t):
    r'\then'
    t.type = reserved.get(t.value, 'THEN')
    return t

# Productions
# Appropriate context free grammar specification
# p = sequence with values of each grammar symbols

# Program
def p_PROGRAM(p):
    '''
    P : WITH P
    '''
    p[0] = p[2]
    print("Interpret Program")

# Statements
def while_loop(t):
    expr = p_E(t[1]) # Get the expression

    # Assert tha loop structure is properly declared
    isValid = t_WHILE(t[1]) and t_LOOP([3]) and t_END(t[5])

    if isValid:
        try:
            loopBody = p_S(t[2])
        except:
            loopBody = p_A(t[2])
    
    while expr:
        eval(loopBody)

def for_loop(t):
    print(t)
    # expr = p_V(t[1]) # Get the variable declaration

    # # Assert that loop structure is properly declared
    # isValid = t_FOR(t[1]) and t_IN(t[3]) and t_LOOP(t[5]) and t_END(t[7])

    # if isValid:
    #     isValidRange = p_R(t[4]) # Assert that range is properly declared
    #     if isValidRange:
    #         loopRange = p_R(t[4]) # Get loop range
    #         try:
    #             loopBody = p_S(t[6])
    #         except:
    #             loopBody = p_A(t[6])
            
    #     for i in loopRange:
    #         eval(loopBody)
     
def if_loop(t):
    expr = p_E(t[1])

def loop_type(t):
    if t_WHILE(t[1]) : while_loop(t)
    elif t_FOR(t[1]) : for_loop(t)
    elif t_IF(t[1]) : if_loop(t)

def call_loop(t):
    print('Finding loop')
    loopType = t[1] # while | for | if elsif else | if else | if   end loop

    if loopType == 'while' : while_loop(t)
    elif loopType == 'for' : for_loop(t)
    else : if_loop(t)

    t[0] = t[1]

def p_IFSTATEMENT(p):
    '''
    IFSTATEMENT : IF E THEN S ELSIF S END IF SEMICOLON NEWLINE
                | IF E THEN S ELSE S END IF SEMICOLON NEWLINE
                | IF E THEN S END IF SEMICOLON NEWLINE
                | IF E THEN S ELSIF A END IF SEMICOLON NEWLINE
                | IF E THEN S ELSE A END IF SEMICOLON NEWLINE
                | IF E THEN A END IF SEMICOLON NEWLINE
                | IF E THEN A ELSIF S END IF SEMICOLON NEWLINE
                | IF E THEN A ELSE S END IF SEMICOLON NEWLINE
                | IF E THEN A ELSIF A END IF SEMICOLON NEWLINE
                | IF E THEN A ELSE A END IF SEMICOLON NEWLINE
    '''
    print(Fore.BLUE + '\nIf loop declared...')

def p_WHILESTATEMENT(p):
    '''
    WHILESTATEMENT : WHILE E LOOP S END LOOP SEMICOLON NEWLINE
                   | WHILE E LOOP A END LOOP SEMICOLON NEWLINE
    '''
    print(Fore.BLUE + '\nWhile loop declared...')

def p_FORSTATEMENT(p):
    '''
    FORSTATEMENT : FOR V IN R LOOP S END LOOP SEMICOLON NEWLINE
                 | FOR V IN R LOOP A END LOOP SEMICOLON NEWLINE
    '''
    print(Fore.BLUE + '\nFor loop declared')

def p_S(p):
    '''
    S : WHILESTATEMENT
      | FORSTATEMENT
      | IFSTATEMENT
    '''
    call_loop(p)
    print(Fore.BLUE + '\nStatement: ' + p[1])

# Assignation
def p_A(p):
    '''
    A : ID ASSIGN E SEMICOLON NEWLINE
      | ID ASSIGN FLOATNUM SEMICOLON NEWLINE
      | ID ASSIGN NUMBER SEMICOLON NEWLINE
    '''

    p[0] = operator_type(p[3])
    print(p[0])
    names[p[1]] = p[3]

# Procedures
def p_P(p):
    '''
    P : PROCEDURE ID IS V END ID SEMICOLON NEWLINE
      | PROCEDURE ID IS BEGIN S END ID SEMICOLON NEWLINE
    '''
    # try:
    #     p[0] = p_V(p[4])
    # except:
    #     p[0] = p_S(p[4])

    p[0] = p[4]
    print(Fore.BLUE + 'Procedure: ' + p[2] + ', declared...' + p[0])
    return p

# Expressions
def operator_type(t):
    op = 0
    try:
        op = t_NUMBER(t)
    except:
        op = t_FLOAT(t)
    return op

def evaluator(t, op1, op2):
    if t == '+' : return op1 + op2
    elif t == '-' : return op1 - op2
    elif t == '/' : return op1 / op2
    elif t == '*' : return op1 * op2
    elif t == '<' : return op1 < op2
    elif t == '>' : return op1 > op2
    elif t == '=' : return op1 == op2

# Quadruples
# def quadruples():


def p_E(p):
    '''
    E : V GT FLOATNUM 
    | V GT NUMBER 
    | V GT V
    | V LT FLOATNUM 
    | V LT NUMBER 
    | V LT V
    | V EQUAL FLOATNUM 
    | V EQUAL NUMBER 
    | V PLUS FLOATNUM 
    | V PLUS NUMBER 
    | V PLUS V
    | V MINUS FLOATNUM 
    | V MINUS NUMBER 
    | V MINUS V
    | V DIVIDE FLOATNUM 
    | V DIVIDE NUMBER 
    | V DIVIDE V
    | V TIMES FLOATNUM 
    | V TIMES NUMBER 
    | V TIMES V
    | V GTE V
    | V GTE NUMBER
    | V GTE FLOATNUM
    | V LTE V
    | V LTE NUMBER
    | V LTE FLOATNUM
    | V AND V
    | V OR V
    | BRAOPEN V AND V BRACLOSE
    | E BRAOPEN V OR V BRACLOSE
    '''

    op1 = operator_type(p[1]) # Define if it's
    op2 = operator_type(p[3]) # integer or float data type
    expr = evaluator(p[2], op1, op2)
    print(Fore.BLUE + 'Expression: ' + str(expr))

    p[0] = expr

    quad.append(p[2])
    quad.append(op1)
    quad.append(op2)
    
# Variables
def data_type(t):
    if t_NUMBER(t) : return t_NUMBER(t)
    elif t_FLOAT(t) : return t_FLOAT(t)
    else : return t_ARRAY(t)

def range_boundaries(values):
    print('Adding values to Array(matrix)')
    matrix = []
    for v in values:
        matrix.append(np.asarray(v))

# Range
def p_R(p):

    '''
    R : BRAOPEN INT SUSPENSIVE INT BRACLOSE 
      | BRAOPEN INT SUSPENSIVE INT COMMA INT SUSPENSIVE INT BRACLOSE
      | BRAOPEN INT SUSPENSIVE INT COMMA INT SUSPENSIVE INT COMMA INT SUSPENSIVE INT BRACLOSE
    '''

    # Regular expression to find all ranges within the token received
    isRangeRegex = '(\(+[0-9]+\.\.\.[0-9]+)+\,*([0-9]+\.\.\.[0-9]+)*\,*([0-9]+\.\.\.[0-9]+\)+)*'

    # Finding all ranges (maximum 3 per ADA specifications)
    tokenizedRanges = np.array(re.findall(isRangeRegex, p[5]))[0] # This way the ranges get stored in the
                                                                  # form of [[range1, range2, range3]], 
                                                                  # therefore we only store the first item
                                                                  # so that we can have single dimension 
                                                                  # array with all declared ranges. 
                                                                  # A string with the ranges is returned. 
                                                                  # Example: (0...4) or (0...4,0...5) or (0...4,0...2,0...5)
    ranges = [] # Empty ranges list

    for r in tokenizedRanges:
        for v in r:
            if v.isnumeric(): ranges.append(v)

    print(Fore.BLUE + '\nArray ranges: ')
    print(ranges)
    return ranges

def p_V(p):
    '''
    V : TYPE ID IS INT SEMICOLON NEWLINE
      | TYPE ID IS FLOAT SEMICOLON NEWLINE
      | TYPE ID IS ARRAY R SEMICOLON NEWLINE
      | TYPE ID SEMICOLON NEWLINE
      | A
    '''    

    if p[2] in names.keys() or p[2] in operands:
        print('\nA variable cannot be declared twice')
    else:
        names[p[2]] = p[4] # Validate when a var is declared without initial value
    
    print(Fore.BLUE + 'Variable declared: ' + str(p))

# Grammar Error Handling
def p_error(t):
    print(Fore.RED + 'Syntax Error in %s' % t.value)
    err.append({'Syntax Error': 'Syntax Error at line ' + str(t.lineno)})

# Building the parser
import ply.yacc as yacc
parser = yacc.yacc()

print(Fore.MAGENTA + 'Analyzing Code...\n')
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = f.read()
while True:
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break   # No more input
        # Token identification correction
        if token.value == 'hen': token.value = 'then'
        # Identifying reserved words
        if token.type in reserved.values(): print(Fore.RESET + 'Reserved word ' + token.value)
        # Arithmetic operations translations
        if token.value in operands: 
            copyOperators = operators.copy()
            # If latest detected operator is not Assign, then we're repeating a variable name
            if copyOperators.pop() != ':=':
                print(Fore.LIGHTRED_EX + '\nVariable cannot be delcared twice.')
                err.append({'ERROR:': 'A variable cannot be declared twice. AT LINE ' + str(token.lineno) })
            else:
                copyOperands = operands.copy()
                names[token.value] = copyOperands.pop()
        elif token.type == 'ID' and token.value not in reserved.keys(): 
            operands.append(token.value)
            names[token.value] = ''
        if token.value not in names: values.append(0) 
        else: values.append(names[token.value])
        # If token is of type operator, we add it to the operators stack
        if token.type in operatorsHelper: 
            operators.append(token.value)
        # If a loop is being declared, we start the loops stack for quadruples
        if token.type in loopsHelper: 
            loops.append(token.value) # Here we add the beginning or end of a loop
            loopCnt+=1 # Increment counter
            jumps.append(loopCnt - 1) # Register jumpç
            if token.type == 'WHILE': whileDirs.append(token.lineno)
        if token.type == operatorsHelper:
            loops.append(token.value)

        print(Fore.LIGHTGREEN_EX + '\nToken found')
        print(token.type, token.value, token.lineno, '\n')
        parsedTokens.append([{ 'Type' : token.type }, { 'Value' : token.value }, { 'Address' : token.lineno }])
    break
result = parser.parse(data)
print(Fore.LIGHTYELLOW_EX + '\nSymbol Table:')
print(names)
SymbolTable.write(str(names))

print(Fore.MAGENTA + '\nAnalysis complete...\n')

# Errors
print(Fore.LIGHTRED_EX + '\nErrors:')
for e in err:
    for errorKey, errorValue in e.items():
        print(Fore.LIGHTRED_EX + errorKey + ': ' + errorValue)
        errorLog.write(str(Fore.LIGHTRED_EX + errorKey + ': ' + errorValue))

# Tokens
print(Fore.LIGHTBLACK_EX + '\n\nTokens')
for parsedToken in parsedTokens:
    print('\n')
    print(Fore.LIGHTWHITE_EX + '*************************************')
    tokenLog.write('\n')
    tokenLog.write(str(Fore.LIGHTWHITE_EX + ':'))
    for pT in parsedToken:
        for key, value in pT.items():
            print(Fore.LIGHTMAGENTA_EX + key + ' ' + str(value))
            tokenLog.write(str(Fore.LIGHTMAGENTA_EX + key + ' ' + str(value)))
            print(Fore.LIGHTMAGENTA_EX + '-------------------------------------')
            tokenLog.write(str(Fore.LIGHTMAGENTA_EX + ';'))
    print(Fore.LIGHTWHITE_EX + '*************************************')
    tokenLog.write(str(Fore.LIGHTWHITE_EX + ':'))

# Expressions
print(Fore.LIGHTWHITE_EX + '\nExpressions: \n')
print('Operands: \n')
print(operands)
print('\n')
print('Operators: \n')
print(operators)

# Quadruples
print(Fore.LIGHTWHITE_EX + '\nQuadruples: \n')
i = 0
t = 0
for operator in operators:
    quad.append(operator)
    quad.append(operands[i])
    if i > len(operands): i = 0
    quad.append(operands[i + 1])
    if operator == ':=': quad.append(operands[i])
    else: quad.append('T' + str(t))
    t+=1

k = 0
while k < len(quad):
    print(quad[k:k+4])
    print('\n')
    Quadruples.write(str(quad[k:k+4]))
    Quadruples.write('\n')
    k+=4

# Loops & Cycles Translations
print(Fore.LIGHTBLACK_EX + '\nLoops and Cycles\n')
j = 0
gotoTrue = ''
quadStr = ''
temp = ''
exprIndex = 0
for loop in loops:
    if (j + 4) > len(quad): j = 0
    quadStr = quad[j:j+4]
    if loop == 'if':
        print(Fore.LIGHTYELLOW_EX + 'for loop...\n')
        print(quadStr)
        print('\n')
        gotoTrue = quadStr[3]
        if loop == 'then':
            # add quadruples
            # goto true
            print('goto ' + gotoTrue + ' ' + str(loopCnt.pop()))
            print('\n')
        elif loop == 'else':
            #End
            jumpIndex = jumps.pop()
            print('gotof ' + quadStr[3] + str(jumpIndex))
            print('\n')
        else:
            # Open Goto
            print("goto '' ''")
            print('\n')
    elif loop == 'while':
        print(Fore.LIGHTYELLOW_EX + 'while loop...\n')
        jumpIndex = jumps.pop()
        exprIndex = quad.index('>') or quad.index('<') or quad.index('<=') or quad.index('>=')
        temp = quad[exprIndex:exprIndex + 4]
        print(quadStr)
        print('\n')
        print('gotof ' + str(quadStr[3]) + ' ' + str(jumpIndex))
        if quadStr != temp: print(quadStr)
        else:
            j+=4
            quadStr = quad[j:j+4]
            print(quadStr)
        print('\n')
        print('goto ' + str(whileDirs))
    j+=4


# Sources:
# https://programmerclick.com/article/9778279087/#1_Preface_and_Requirements_2
# https://www.adaic.org/resources/add_content/standards/05aarm/html/AA-2-9.html
# https://ericknavarro.io/2020/02/10/24-Mi-primer-proyecto-utilizando-PLY/
# https://regex101.com/
# https://www.w3schools.com/python/python_regex.asp
# https://alexgaynor.net/2008/nov/10/getting-started-ply-part-3/