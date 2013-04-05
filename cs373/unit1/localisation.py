pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def make_prob_vector(n):
    return [1.0/n for _ in range(n)]

def get_probs(p):
    return [prob for (_, prob) in p]

def get_objs(p):
    return [obj for (obj, _) in p]

def sense(p, Z):
    q = [prob * pHit if obj == Z else prob * pMiss for (obj, prob) in p]
    return zip(get_objs(p), [prob/sum(q) for prob in q])

def move(p, places):
    probs = get_probs(p)
    q = []
    for i in range(len(probs)):
        exact = probs[(i-places) % len(probs)] * pExact
        over = probs[(i-places+1) % len(probs)] * pOvershoot
        under = probs[(i-places-1) % len(probs)] * pUndershoot
        q.append(sum([exact, under, over]))
    return zip(get_objs(p), q)


world = ['green','red','red','green','green']
initial_distribution = make_prob_vector(len(world))
measurements = ['red','red']
motions = [1,1]

p = zip(world, initial_distribution)

for i in range(len(measurements)):
    p = sense(p, measurements[i])
    p = move(p, motions[i])

print get_probs(p)
