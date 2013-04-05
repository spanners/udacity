# Implementing RE
# Challenge Problem 
#
# Focus: All Units
#
#
# In this problem you will write a lexer, parser and interpreter for
# strings representing regular expressions. Your program will output 
# a non-deterministic finite state machine that accepts the same language
# as that regular expression. 
#
# For example, on input 
#
# ab*c
#
# Your program might output
# 
# edges = { (1,'a')  : [ 2 ] ,
#           (2,None) : [ 3 ] ,    # epsilon transition
#           (2,'b')  : [ 2 ] ,
#           (3,'c')  : [ 4 ] } 
# accepting = [4]
# start = 1
#
# We will consider the following regular expressions:
#
#       single characters       #       a       
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b) 
#
# That's it. We won't consider [a-c] because it's just a|b|c, and we won't
# consider a+ because it's just aa*. We will not worry about escape
# sequences. Single character can be a-z, A-Z or 0-9 -- that's it. No need
# to worry about strange character encodings. We'll use ( ) for regular
# expression grouping instead of (?: ) just to make the problem simpler.
#
# Don't worry about precedence or associativity. We'll fully parenthesize
# all regular expressions before giving them to you. 
#
# You will write a procedure re_to_nfsm(re_string). It takes as input a
# single argument -- a string representing a regular expression. It returns
# a tuple (edges,accepting,start) corresponding to an NSFM that accepts the
# same language as that regular expression.
#
# Hint: Make a lexer and a paser and an interpreter. Your interpreter may
# find it handy to know the current state and the goal state. Make up as
# many new states as you need. 
# 
import ply.lex as lex
import ply.yacc as yacc

# Fill in your code here. 

### LEXER ###

tokens = (
        'ZEROMORE', # *
        'OR',       # |
        'LETTER',   # a-z
        'LPAREN',   # (
        'RPAREN'    # )
        )

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ZEROMORE = r'\*'
t_OR = r'\|'
t_LETTER = r'[a-z]'

def t_error(t):
        print "RegExp Lexer: Illegal character " + t.value[0]
        t.lexer.skip(1)

### PARSER ###
#       single characters       #       a       
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b) 

start = 're'

precedence = (
        # lower precedence --^
        ('left', 'OR'),
        ('left', 'SEQUENCE'),
        ('left', 'ZEROMORE'),
        # higher precedence --\/
        )

def p_re_letter(p):
    're : LETTER %prec SEQUENCE'
    p[0] = ("letter", p[1])

def p_re_sequence(p):
    're : re re %prec SEQUENCE'
    p[0] = ("sequence", p[1], p[2])

def p_re_or(p):
    're : re OR re'
    p[0] = ("or", p[1], p[3])

def p_re_group(p):
    're : LPAREN re RPAREN'
    p[0] = p[2]

def p_re_zeromore(p):
    're : re ZEROMORE'
    p[0] = ("zeromore", p[1])

def p_error(p):
    raise SyntaxError

### INTERPRETER ###

EPSILON = None
NUM_STATES = 3

def add_state(edges, curr, goal, letter):
    """ Prevents clobbering edges.
    Either append if existing or create new edge. """
    if (curr, letter) in edges:
        edges[(curr, letter)] = edges[(curr, letter)] + [goal]
    else:
        edges[(curr, letter)] = [goal]

def increment_state_num():
    """ Tracks the number of states created """
    global NUM_STATES
    curr_num = NUM_STATES
    NUM_STATES = NUM_STATES + 1
    return curr_num

def eval_re(re, edges, curr, goal):
    """ Recursively evaluate a regular expression tree. """
    retype = re[0]
    if retype == 'letter':
        add_state(edges, curr, goal, re[1])
    elif retype == 'sequence':
        state = increment_state_num()
        eval_re(re[1], edges, curr, state)
        eval_re(re[2], edges, state, goal)
    elif retype == 'or':
        eval_re(re[1], edges, curr, goal)
        eval_re(re[2], edges, curr, goal)
    elif retype == 'zeromore':
        add_state(edges, curr, goal, EPSILON)
        eval_re(re[1], edges, curr, curr)
    else:
        print "RegExp Interpreter Error:" + re

def interpret(ast):
    start_state = 1
    accepting = [2]
    edges = {}
    eval_re(ast, edges, start_state, accepting[0])
    result = (edges, accepting, start_state)
    # print result
    return result



########################

lexer = lex.lex()
parser = yacc.yacc()

def re_to_nfsm(re_string):
        # Feel free to overwrite this with your own code. 
        lexer.input(re_string)
        parse_tree = parser.parse(re_string, lexer=lexer)
        return interpret(parse_tree)

# We have included some testing code ... but you really owe it to yourself
# to do some more testing here.

def nfsmaccepts(edges, accepting, current, string, visited):
        # If we have visited this state before, return false. 
        if (current, string) in visited:
                return False
        visited.append((current, string))

        # Check all outgoing epsilon transitions (letter == None) from this
        # state. 
        if (current, None) in edges:
                for dest in edges[(current, None)]:
                        if nfsmaccepts(edges, accepting, dest, string, visited):
                                return True

        # If we are out of input characters, check if this is an
        # accepting state. 
        if string == "":
                return current in accepting

        # If we are not out of input characters, try all possible
        # outgoing transitions labeled with the next character. 
        letter = string[0]
        rest = string[1:]
        if (current, letter) in edges:
                for dest in edges[(current, letter)]:
                        if nfsmaccepts(edges, accepting, dest, rest, visited):
                                return True
        return False

def test(re_string, e, ac_s, st_s, strings):
  my_e, my_ac_s, my_st_s = re_to_nfsm(re_string)
  for string in strings:
      print string, nfsmaccepts(e,ac_s,st_s,string,[]) == \
            nfsmaccepts(my_e,my_ac_s,my_st_s,string,[])

edges = { (1,'a')  : [ 2 ] ,
          (2,None) : [ 3 ] ,    # epsilon transition
          (2,'b')  : [ 2 ] ,
          (3,'c')  : [ 4 ] }
accepting_state = [4]
start_state = 1

test("a(b*)c", edges, accepting_state, start_state,
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  )

edges = { (1,'a')  : [ 2 ] ,
          (2,'b') :  [ 1 ] ,
          (1,'c')  : [ 3 ] ,
          (3,'d')  : [ 1 ] }
accepting_state = [1]
start_state = 1

test("((ab)|(cd))*", edges, accepting_state, start_state,
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  )
