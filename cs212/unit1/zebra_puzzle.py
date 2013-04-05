"""
The Zebra Puzzle http://en.wikipedia.org/wiki/Zebra_Puzzle

#1 There are five houses.
#2 The Englishman lives in the red house.
#3 The Spaniard owns the dog.
#4 Coffee is drunk in the green house.
#5 The Ukrainian drinks tea.
#6 The green house is immediately to the right of the ivory house.
#7 The Old Gold smoker owns snails.
#8 Kools are smoked in the yellow house.
#9 Milk is drunk in the middle house.
#10 The Norwegian lives in the first house.
#11 The man who smokes Chesterfields lives in the house next to the man with the fox.
#12 Kools are smoked in the house next to the house where the horse is kept. [should be "... a house ...", see discussion below]
#13 The Lucky Strike smoker drinks orange juice.
#14 The Japanese smokes Parliaments.
#15 The Norwegian lives next to the blue house.

Now, who drinks water? Who owns the zebra? In the interest of clarity, it must be added that each of the five houses is painted a different color, and their inhabitants are of different national extractions, own different pets, drink different beverages and smoke different brands of American cigarets [sic]. One other thing: in statement 6, right means your right.
"""

import itertools

def imright(h1, h2):
    "House h1 is immediately right of h2 if h1-h2 == 1."
    return h1-h2 == 1

def nextto(h1, h2):
    "Two houses are next to each other if they differ by 1."
    return abs(h1-h2) == 1

def zebra_puzzle():
    "Return a tuple (WATER, ZEBRA indicating their house numbers."
    houses = first, _, middle, _, _ = [1, 2, 3, 4, 5] #1
    orderings = list(itertools.permutations(houses))
    return next((WATER, ZEBRA)
                for (red, green, ivory, yellow, blue) in c(orderings)
                if imright(green, ivory) #6
                for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in c(orderings)
                if Englishman is red #2
                if Norwegian is first #10
                if nextto(Norwegian, blue) #15
                for (coffee, tea, milk, oj, WATER) in c(orderings)
                if coffee is green #4
                if Ukranian is tea #5
                if milk is middle #9
                for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in c(orderings)
                if Kools is yellow #8
                if LuckyStrike is oj #13
                if Japanese is Parliaments #14
                for (dog, snails, fox, horse, ZEBRA) in c(orderings)
                if Spaniard is dog #3
                if OldGold is snails #7
                if nextto(Chesterfields, fox) #11
                if nextto(Kools, horse) #12
                )

import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers))

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    times = []
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timedcall(fn, *args)[0])
    return min(times), average(times), max(times)

def c(sequence):
    """Generate items in sequence; keeping counts as we go. c.starts is the
    number of sequences started; c.items is number of items generated."""
    c.starts += 1
    for item in sequence:
        c.items += 1
        yield item

def instrument_fn(fn, *args):
    """Count the number of calls it takes to execute the calling of function fn
    with the arguments args."""
    c.starts, c.items = 0, 0
    result = fn(*args)
    return '%s got %s with %5d iters over %7d items' % (
            fn.__name__, result, c.starts, c.items)

print(instrument_fn(zebra_puzzle))
