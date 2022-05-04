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
    'then' : 'THEN'
}

tokens = [
    'ID', 
    #'FLOAT',
    #'INT',
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
t_EQUAL = r'='
t_TIMES = r'\*'
t_GT = r'>'
t_LT = r'<'

# Special Tokens
t_SEMICOLON = r'\;'
t_ASSIGN = r':='
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
names = { }

# Token Functions
# Regex definition in functions. This implemenation is useful because
# it allows us to manipulate the value of the token received.

# Variable Id
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    print(Fore.GREEN + '\nID: ' + t.value)
    
    #if not (t.value in reserved.values()) or  not (t.value in tokens): names[t.value] = ''
    return t

# type
def t_TYPE(t):
    r'type'
    t.type = reserved.get(t.value, 'TYPE')
    print(Fore.GREEN + 'Variable type being identified...')
    return t

# is
def t_IS(t):
    r'is'
    t.type = reserved.get(t.value, 'IS')
    print(Fore.GREEN + '\nis of type...')
    return t

# Integers
def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(Fore.RED + 'Value too large %d', t.value)
    
    print(Fore.GREEN + '\nInteger of value: ' + str(t.value))
    return t

# Floats
def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(Fore.RED + 'Value too large %d', t.value)
        t.value = 0
    
    print(Fore.GREEN + '\nFloat of value: ' + str(t.value))
    return t

# use
def t_USE(t):
    r'use'
    t.type = reserved.get(t.value, 'USE')
    print(Fore.BLUE + '\nNew Context declared...')
    return t

# procedure
def t_PROCEDURE(t):
    r'procedure'
    t.type = reserved.get(t.value, 'PROCEDURE')
    print(Fore.BLUE + '\nProcedure delcared...')
    return t

# Characters to ignore
# t_ prefix for python's native library to identify a token as a regex

# Tab
def t_TAB(t):
    r' \t'
    t.lexer.lineno += t.value.count('\t')
    print(Fore.BLUE + '\nSkipped tab...')
    pass

# New Line
def t_NEWLINE(t):
    r' \n'
    t.lexer.lineno += t.value.count('\n')
    print(Fore.BLUE + '\nSkipped new line...')
    pass

# Comment
def t_comment(t):
    r'\--'
    pass

# Error Handling
def t_error(t):
    print(Fore.RED + 'Illegal character %s' % t.value[0] + t.type)
    t.lexer.skip(1)

# Building the lexer
import ply.lex as lex
lexer = lex.lex()

# Syntax Rules

# Array
def t_ARRAY(t):
    r'array'
    t.type = 'ARRAY'
    print(Fore.BLUE + '\nArray declared...')
    return t

# begin
def t_BEGIN(t):
    r'begin'
    t.type = reserved.get(t.value, 'BEGIN')
    print(Fore.BLUE + '\nBegin procedure')
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
    r'then'
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
    # '''
    # P : WITH C USE C P
    #   | WITH C P
    #   | WITH P
    # '''
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
    expr = p_V(t[1]) # Get the variable declaration

    # Assert that loop structure is properly declared
    isValid = t_FOR(t[1]) and t_IN(t[3]) and t_LOOP(t[5]) and t_END(t[7])

    if isValid:
        isValidRange = p_R(t[4]) # Assert that range is properly declared
        if isValidRange:
            loopRange = p_R(t[4]) # Get loop range
            try:
                loopBody = p_S(t[6])
            except:
                loopBody = p_A(t[6])
            
        for i in loopRange:
            eval(loopBody)
     
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

def p_S(p):
    '''
    S : WHILE E LOOP S END LOOP SEMICOLON
      | WHILE E LOOP A END LOOP SEMICOLON 
      | FOR V IN R LOOP S END LOOP SEMICOLON 
      | FOR V IN R LOOP A END LOOP SEMICOLON 
      | IF E THEN S ELSIF S END IF SEMICOLON 
      | IF E THEN S ELSE S END IF SEMICOLON 
      | IF E THEN S END IF SEMICOLON
      | IF E THEN S ELSIF A END IF SEMICOLON 
      | IF E THEN S ELSE A END IF SEMICOLON 
      | IF E THEN A END IF SEMICOLON 
      | IF E THEN A ELSIF S END IF SEMICOLON 
      | IF E THEN A ELSE S END IF SEMICOLON 
      | IF E THEN A ELSIF A END IF SEMICOLON
      | IF E THEN A ELSE A END IF SEMICOLON
    '''
    call_loop(p)
    print(Fore.BLUE + '\nStatement: ' + p[1])

# Assignation
def p_A(p):
    '''
    A : V ASSIGN E SEMICOLON 
      | V ASSIGN FLOAT SEMICOLON 
      | V ASSIGN INT SEMICOLON
    '''

    p[0] = operator_type(p[3])
    print(p[0])
    index = names.keys().index(p[1])
    names[index] = p[3]

# Procedures
def p_P(p):
    '''
    P : PROCEDURE ID IS V END ID SEMICOLON 
      | PROCEDURE ID IS BEGIN S END ID
    '''
    try:
        p[0] = p_V(p[4])
    except:
        p[0] = p_S(p[4])

    print(Fore.BLUE + 'Procedure: ' + p[2] + ', declared...' + p[0])
    return p

# Expressions
def operator_type(t):
    op = 0
    try:
        op = t_INT(t)
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

def p_E(p):
    '''
    E : V GT FLOAT 
    | V GT INT 
    | V GT V
    | V LT FLOAT 
    | V LT INT 
    | V LT V
    | V EQUAL FLOAT 
    | V EQUAL INT 
    | V PLUS FLOAT 
    | V PLUS INT 
    | V PLUS V
    | V MINUS FLOAT 
    | V MINUS INT 
    | V MINUS V
    | V DIVIDE FLOAT 
    | V DIVIDE INT 
    | V DIVIDE V
    | V TIMES FLOAT 
    | V TIMES INT 
    | V TIMES V
    | V GTE V
    | V GTE INT
    | V GTE FLOAT
    | V LTE V
    | V LTE INT
    | V LTE FLOAT
    '''

    op1 = operator_type(p[1]) # Define if it's
    op2 = operator_type(p[3]) # integer or float data type
    expr = evaluator(p[2], op1, op2)
    print(Fore.BLUE + 'Expression: ' + str(expr))

    p[0] = expr

    if p[2] == '+' : p[0] = p[1] + p[3]
    elif p[2] == '-' : p[0] = p[1] - p[3]
    elif p[2] == '/' : p[0] = p[1] / p[3]
    elif p[2] == '*' : p[0] = p[1] * p[3]
    elif p[2] == '<' : p[0] = p[1] < p[3]
    elif p[2] == '>' : p[0] = p[1] > p[3]
    elif p[2] == '=' : p[0] = p[1] == p[3]

    names[p[0]] = expr

# Variables
def data_type(t):
    if t_INT(t) : return t_INT(t)
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
    V : TYPE ID IS INT SEMICOLON 
      | TYPE ID IS FLOAT SEMICOLON
      | TYPE ID IS ARRAY R SEMICOLON
      | TYPE ID SEMICOLON
    '''    

    if p[4] in names():
        print('\nA variable cannot be declared twice')
    
    print(Fore.BLUE + 'Variable declared: ' + str(p))

    p[0] = p[4]
    names[p[0]] = p[4]

# Grammar Error Handling
def p_error(t):
    print(Fore.RED + 'Syntax Error in %s' % t.value)

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
        
        if token.value in reserved.values(): print('Reserved word')

        print(Fore.GREEN + '\nToken found')
        print(token.type, token.value, token.lineno, '\n')
    break
result = parser.parse(data)
print(Fore.YELLOW + 'Symbol Table: \n')
print(names)
print(Fore.MAGENTA + 'Analysis complete...')

# Sources:
# https://programmerclick.com/article/9778279087/#1_Preface_and_Requirements_2
# https://www.adaic.org/resources/add_content/standards/05aarm/html/AA-2-9.html
# https://ericknavarro.io/2020/02/10/24-Mi-primer-proyecto-utilizando-PLY/
# https://regex101.com/
# https://www.w3schools.com/python/python_regex.asp
# https://alexgaynor.net/2008/nov/10/getting-started-ply-part-3/

# Range Regex Explanation

# 1st Capturing Group ([0-9]+\.\.\.[0-9]+)+\,*([0-9]+\.\.\.[0-9]+)*\,*([0-9]+\.\.\.[0-9]+)*

# Match a single character present in the list below [0-9]
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# 0-9 matches a single character in the range between 0 (index 48) and 9 (index 57) (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)

# Match a single character present in the list below [0-9]
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# 0-9 matches a single character in the range between 0 (index 48) and 9 (index 57) (case sensitive)
# \, matches the character , with index 4410 (2C16 or 548) literally (case sensitive)
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)

# Match a single character present in the list below [0-9]
# 0-9 matches a single character in the range between 0 (index 48) and 9 (index 57) (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)

# Match a single character present in the list below [0-9]
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# 0-9 matches a single character in the range between 0 (index 48) and 9 (index 57) (case sensitive)
# \, matches the character , with index 4410 (2C16 or 548) literally (case sensitive)

# Match a single character present in the list below [0-9]
# 0-9 matches a single character in the range between 0 (index 48) and 9 (index 57) (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# Match a single character present in the list below [0-9]
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# 0-9 matches a single character in the range between 0 (index 48) and 9 (index 57) (case sensitive)

# Global pattern flags 
# g modifier: global. All matches (don't return after first match)
# m modifier: multi line. Causes ^ and $ to match the begin/end of each line (not only begin/end of string)