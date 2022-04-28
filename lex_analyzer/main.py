# A01411195   Soraya Lizeth Maqueda Gutiérrez
# Lenguajes y Traductores - Analizador de Léxico

# Ply tools to create lexic analyzer
import numpy as np
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
    #'range' : 'RANGE',
    'type' : 'TYPE',
    'use' : 'USE',
    'with' : 'WITH',
    'while' : 'WHILE',
    'then' : 'THEN'
}

tokens = [
    'ID', 
    'FLOAT',
    'INT',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'TIMES',
    'GT',
    'GTE',
    'LT',
    'LTE',
    'SEMICOLON',
    'EQUAL',
    'SUSPENSIVE',
    'COMMA',
    'BRAOPEN',
    'BRACLOSE'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'/'
t_LTE = r'\<='
t_GTE = r'\>='
t_EQUAL = r'\='
 
# Precedence 
# By default, there's an ambiguety as to the expression syntax, therefore yacc allows
# us to set a precedence an associate it to individaul tags.
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# Dictionary for Variable Names
names = { }

# Characters to ignore
# t_ prefix for python's native library to identify a token as a regex

# Tab
def t_tab(t):
    r'\t'
    t.lexer.lineno += t.value.count('\t')
    pass

# New Line
def t_newLine(t):
    r'\n'
    t.lexer.lineno += t.value.count('\n')
    pass

# Comment
def t_comment(t):
    r'\--'
    pass

# Error Handling
def t_error(t):
    print('Illegal character %s' % t.value[0])
    t.lexer.skip(1)

# Building the lexer
import ply.lex as lex
lexer = lex.lex()

# Token Functions
# Regex definition in functions. This implemenation is useful because
# it allows us to manipulate the value of the token received.

# Aritmetic Operators
def t_TIMES(t):
    r'\*'
    t.type = 'TIMES'
    return t

def t_LT(t):
    r'<'
    t.type = 'LT'
    return t

def t_GT(t):
    r'>'
    t.type = 'GT'
    return t

# Integers
def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print('Value too large %d', t.value)
    return t

# Floats
def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print('Value too large %d', t.value)
        t.value = 0
    return t

# Special Tokens

# Assign
def t_ASSIGN(t):
    r'\:='
    t.type = ':='
    return t

def t_SUSPENSIVE(t):
    r'\...'
    t.type = 'SUSPENSIVE'
    return t

def t_COMMA(t):
    r'\,'
    t.type = 'COMMA'
    return t

def t_BRAOPEN(t):
    r'\('
    t.type = 'BRAOPEN'
    return t

def t_BRACLOSE(t):
    r'\)'
    t.type = 'BRACLOSE'
    return t

# Syntax Rules

# Array
def t_ARRAY(t):
    r'array'
    t.type = 'ARRAY'
    return t

# begin
def t_BEGIN(t):
    r'begin'
    t.type = 'BEGIN'
    return t

# else
def t_ELSE(t):
    r'else'
    t.type = 'ELSE'
    return t

# elsif
def t_ELSIF(t):
    r'elsif'
    t.type = 'ELSIF'
    return t

# end
def t_END(t):
    r'end'
    t.type = 'END'
    return t

# for
def t_FOR(t):
    r'for'
    t.type = 'FOR'
    return t

# if
def t_IF(t):
    r'if'
    t.type = 'IF'
    return t

# in
def t_IN(t):
    r'in'
    t.type = 'IN'
    return t

# is
def t_IS(t):
    r'is'
    t.type = 'IS'
    return t

# loop
def t_LOOP(t):
    r'loop'
    t.type = 'LOOP'
    return t

# procedure
def t_PROCEDURE(t):
    r'procedure'
    t.type = 'PROCEDURE'
    return t

# range
# def t_RANGE(t):
#     isRangeRegex = '(\(+[0-9]+\.\.\.[0-9]+)+\,*([0-9]+\.\.\.[0-9]+)*\,*([0-9]+\.\.\.[0-9]+\)+)*'
#     ranges = re.search(isRangeRegex, t).group() # A string with the ranges is returned. 
#                                                 # Example: (0...4) or (0...4,0...5) or (0...4,0...2,0...5)
#     t.type = 'RANGE'
#     return t, ranges

# type
def t_TYPE(t):
    r'type'
    t.type = 'TYPE'
    return t

# use
def t_USE(t):
    r'use'
    t.type = 'USE'
    return t

# with
def t_WITH(t):
    r'with'
    t.type = 'WITH'
    return t

# while
def t_WHILE(t):
    r'while'
    t.type = 'WHILE'
    return t

# Variable Id
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    print(t[1])
    return t

# Semicolon
def t_SEMICOLON(t):
    r';'
    t.type = ';'
    return t

# Productions
# Appropriate context free grammar specification
# p = sequence with values of each grammar symbols

# Program
def p_PROGRAM(t):
    '''
    P : WITH P
    '''
    # '''
    # P : WITH C USE C P
    #   | WITH C P
    #   | WITH P
    # '''
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
        isValidRange = t_RANGE(t[4]) # Assert that range is properly declared
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

def p_S(t):
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
    call_loop(t)
    #t[0] = t[1]

# Assignation
def p_A(t):
    '''
    A : V ASSIGN E SEMICOLON 
      | V ASSIGN FLOAT SEMICOLON 
      | V ASSIGN INT SEMICOLON
    '''

    t[0] = operator_type(t[3])

# Procedures
def p_P(t):
    '''
    P : PROCEDURE ID IS V END ID SEMICOLON 
      | PROCEDURE ID IS BEGIN S END ID
    '''
    try:
        t[0] = p_V(t[4])
    except:
        t[0] = p_S(t[4])

    return t

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

def p_E(t):
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

    op1 = operator_type(t[1]) # Define if it's
    op2 = operator_type(t[3]) # integer or float data type
    expr = evaluator(t[2], op1, op2)
    
    t[0] = expr

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
def p_R(t):

    '''
    R : BRAOPEN INT SUSPENSIVE INT BRACLOSE 
      | BRAOPEN INT SUSPENSIVE INT COMMA INT SUSPENSIVE INT BRACLOSE
      | BRAOPEN INT SUSPENSIVE INT COMMA INT SUSPENSIVE INT COMMA INT SUSPENSIVE INT BRACLOSE
    '''

    # Regular expression to find all ranges within the token received
    isRangeRegex = '(\(+[0-9]+\.\.\.[0-9]+)+\,*([0-9]+\.\.\.[0-9]+)*\,*([0-9]+\.\.\.[0-9]+\)+)*'

    # Finding all ranges (maximum 3 per ADA specifications)
    tokenizedRanges = np.array(re.findall(isRangeRegex, t[5]))[0] # This way the ranges get stored in the
                                                                # form of [[range1, range2, range3]], 
                                                                # therefore we only store the first item
                                                                # so that we can have single dimension 
                                                                # array with all declared ranges. 
                                                                # A string with the ranges is returned. 
                                                                # Example: (0...4) or (0...4,0...5) or (0...4,0...2,0...5)
    ranges = [] # Empty ranges list

    for r in ranges:
        for v in r:
            if v.isnumeric(): ranges.append(v)

    return ranges

# Variables
def p_V(t):
    '''
    V : TYPE ID IS INT SEMICOLON 
      | TYPE ID IS FLOAT SEMICOLON 
      | TYPE ID IS ARRAY R SEMICOLON
    '''    
    # Assert variable declaration sytnax is written correctly
    isValid = t_TYPE(t[1]) and t_ID(t[2]) and t_IS(t[3]) and (t_SEMICOLON(t[5]) or t_SEMICOLON(t[6]))
    # Determine if variable declared zoomis array with range
    isArray = t_ARRAY(t[4]) #and t_RANGE(t[5])
    
    if not isArray:
        names[t[2]] = t[4]
    else:
        ranges = p_R(t)  # Get Ranges
        names[t[2]] = ranges
    
    t[0] = t[4]
    print(names)

# Grammar Error Handling
def p_error(t):
    print('Syntax Error in %s' % t.value)

# Building the parser
import ply.yacc as yacc
parser = yacc.yacc()

# Reading file with example code
f = open('./example2.txt', 'r', encoding="utf8")
input = f.read()
print('\n')
print(input)
print('\n')
parser.parse(input)

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