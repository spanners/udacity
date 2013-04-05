#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code around lines 28 and 44
# Do not modify the __repr__ functions.
# Modify only the classes Range and Invariants,
# if you need additional functions, make sure
# they are inside the classes.

import sys
import math
import random

def square_root(x, eps = 0.00001):
    assert x >= 0
    y = math.sqrt(x)
    #assert abs(square(y) - x) <= eps
    return y
    
def square(x):
    return x * x

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self):
        self.min  = None  # Minimum value seen
        self.max  = None  # Maximum value seen
    
    # Invoke this for every value
    def track(self, value):
        if self.min == None and self.max == None:
            self.min = self.max = value
        if self.min >= value or self.max <= value:
            if value <= self.min:
                self.min = value
            elif value >= self.max:
                self.max = value
        else:
            print self.min, self.max, value
            raise AssertionError
            
    def __repr__(self):
        return repr(self.min) + ".." + repr(self.max)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}
        
    def track(self, frame, event, arg):
        if event == "call" or event == "return":
            
            #frame.f_code.co_name # current executing function
            #frame.f_locals # dict of all local vars. if event return, arg gives value
            self.vars[frame.f_code.co_name] = {}
            self.vars[frame.f_code.co_name][event] = {}
            print self.vars
            if event == "return":
                if "ret" not in self.vars[frame.f_code.co_name][event]:
                    self.vars[frame.f_code.co_name][event]["ret"] = Range() 
                self.vars[frame.f_code.co_name][event]["ret"].track(arg)
                print self.vars[frame.f_code.co_name][event]["ret"]
            elif event == "call":
                for var in frame.f_locals:
                    print var, frame.f_locals[var]
                    if var not in self.vars[frame.f_code.co_name][event]:
                        self.vars[frame.f_code.co_name][event][var] = Range()
                    self.vars[frame.f_code.co_name][event][var].track(frame.f_locals[var])
                    print "srsly", self.vars[frame.f_code.co_name][event][var]
            
            # YOUR CODE HERE. 
            # MAKE SURE TO TRACK ALL VARIABLES AND THEIR VALUES
            # If the event is "return", the return value
            # is kept in the 'args' argument to this function.
            # Use it to keep track of variable "ret" (return)
    
    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.iteritems():
            for event, vars in events.iteritems():
                s += event + " " + function + ":\n"
                # continue
                
                for var, range in vars.iteritems():
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"
                
        return s

invariants = Invariants()
    
def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
for i in range(1, 10):
    r = int(random.random() * 1000) # An integer value between 0 and 999.99
    z = square_root(r, eps)
    #z = square(z)
sys.settrace(None)
print invariants


