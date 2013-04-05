chart = { }
def csuffix(X,Y):
    if (X,Y) in chart:
        return chart[(X,Y)]
    else:
        answer = 0
        if X != "" and Y != "" and X[-1:] == Y[-1:]:
            answer = 1 + csuffix(X[:-1],Y[:-1])
        return answer

def prefixes(X):
    return [X[:i+1] for i in range(len(X))]

def lsubstring(X,Y):
    return max([csuffix(i,j) for i in prefixes(X) for j in prefixes(Y)])

print lsubstring("Tapachula", "Temapache")
