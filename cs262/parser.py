def addtochart(theset,index,elt):
    """ Uniquely adds elt to theset at index. """
    if not (elt in theset[index]):
        theset[index] = [elt] + theset[index]
        return True
    return False

def closure(grammar, i, x, ab, cd):
    """ Predict what the next states will be,
    based on the next token to be consumed. """
    LHS, RHS = lambda _: _[0], lambda _: _[1]
    next_states = [\
            (LHS(rule), [], RHS(rule), i) \
            for rule in grammar \
            if cd != [] and LHS(rule) == cd[0]\
            ]
    return next_states

def shift (tokens, i, x, ab, cd, j):
    """ Consume next token in the input if non-terminal. """
    if cd != [] and cd[0] == tokens[i]:
        return (x, ab + [cd[0]], cd[1:], j)
    return None

def reductions(chart, i, x, ab, cd, j):
    """ Reduce by applying the rule x -> ab in reverse. """
    return [\
     (jstate[0], jstate[1] + [x], jstate[2][1:], jstate[3])\
     for jstate in chart[j]\
     if cd == [] and jstate[2] != [] and jstate[2][0] == x
     ]

def parse(tokens,grammar,verbose=False):
    """ Parse tokens and determine if they're in the grammar. """
    tokens = tokens + ["end_of_input_marker"]
    chart = {}
    start_rule = grammar[0]
    for i in range(len(tokens)+1): # initialise the chart
	chart[i] = []
    start_state = (start_rule[0], [], start_rule[1], 0)
    chart[0] = [start_state]
    for i in range(len(tokens)):
        while True:
            changes = False
            for state in chart[i]:
                # State === x -> ab . cd, j
                x,ab,cd,j = state
                next_states = closure(grammar,i,x,ab,cd)
                for next_state in next_states:
                    changes = addtochart(chart,i,next_state) or changes
                next_state = shift(tokens,i,x,ab,cd,j)
                if next_state != None:
                    changes = addtochart(chart,i+1,next_state) or changes
                next_states = reductions(chart,i,x,ab,cd,j)
                for next_state in next_states:
                    changes = addtochart(chart,i,next_state) or changes
            if not changes: break
    if verbose: print_chart(tokens,chart)
    accepting_state = (start_rule[0], start_rule[1], [], 0)
    return accepting_state in chart[len(tokens)-1]

def print_chart(tokens,chart):
    """ Print out the chart. """
    for i in range(len(tokens)):
        print "== chart " + str(i)
        for state in chart[i]:
            x,ab,cd,j = state
            print "	" + x + " ->",
            for sym in ab:
                print " " + sym,
            print " .",
            for sym in cd:
                print " " + sym,
            print "  from " + str(j)

import grammar, tokens
result = parse(tokens.tokens,grammar.grammar, True)

print result
