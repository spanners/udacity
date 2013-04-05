import ply.lex as lex
import ply.yacc as yacc
import graphics as graphics
import jstokens
import jsgrammar
import jsinterp 
import htmltokens
import htmlgrammar

# Load up the lexers and parsers that you have already written in
# previous assignments. Do not worry about the "module" or 
# "tabmodule" arguments -- they handle storing the JavaScript
# and HTML rules separately. 
htmllexer  = lex.lex(module=htmltokens) 
htmlparser = yacc.yacc(module=htmlgrammar,tabmodule="parsetabhtml") 
jslexer    = lex.lex(module=jstokens) 
jsparser   = yacc.yacc(module=jsgrammar,tabmodule="parsetabjs") 

def optimize(exp):
    etype = exp[0]
    if etype == "binop":
        a = optimize(exp[1])
        op = exp[2]
        b = optimize(exp[3])
        # Try Arithmetic Laws
        if op == "*" and (a == ("number",0) or b == ("number",0)):
            return ("number",0)
        elif op == "*" and a == ("number",1):
            return b
        elif op == "*" and b == ("number",1):
            return a
        elif op == "+" and a == ("number",0):
            return b
        elif op == "+" and b == ("number",0):
            return a
        elif op == "-" and a == b:
            return ("number",0)

        if a[0] == "number" and b[0] == "number":
            if op == "+":
                return ("number", a[1]+b[1])
            elif op == "-":
                ("number", a[1]-b[1])
            elif op == "*":
                ("number", a[1]*b[1])

        return ("binop",a,op,b)

    return exp

# The heart of our browser: recursively interpret an HTML abstract
# syntax tree. 
def interpret(ast):     
        for node in ast:
                nodetype = node[0]
                if nodetype == "word-element":
                        graphics.word(node[1]) 
                elif nodetype == "tag-element":
                        tagname = node[1];
                        tagargs = node[2];
                        subast = node[3];
                        closetagname = node[4]; 
                        if (tagname <> closetagname):
                                graphics.warning("(mistmatched " + tagname + " " + closetagname + ")")
                        else: 
                                graphics.begintag(tagname,tagargs);
                                interpret(subast)
                                graphics.endtag(); 
                elif nodetype == "javascript-element": 
                        jstext = node[1]; 
                        jsast = jsparser.parse(jstext,lexer=jslexer) 
                        optimizedast = optimize(jsast) or jsast
                        result = jsinterp.interpret(optimizedast)
                        htmlast = htmlparser.parse(result,lexer=htmllexer)
                        interpret(htmlast)

# Here is an example webpage that includes JavaScript that generates HTML.
# You can use it for testing.
import sys
webpage = open(sys.argv[1], "r")
content = webpage.read()
webpage.close()
htmlast = htmlparser.parse(content,lexer=htmllexer) 
graphics.initialize() # let's start rendering a webpage
interpret(htmlast) 
graphics.finalize() # we're done rendering this webpage

