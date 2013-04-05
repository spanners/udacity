def nfsmsim(string, current, edges, accepting):
    if string == "":
        return current in accepting
    else:
        letter = string[0]
        if (current, letter) in edges:
            return any([nfsmsim(string[1:],state,edges,accepting) for state in edges[(current, letter)]])
        else:
            return False
