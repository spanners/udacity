colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

def calculate():
    m=len(colors)
    n=len(colors[0])
    p=[[1./(m*n)]*n]*m
    def norm(p): 
        return [[i/float(sum(map(sum,p))) for i in r] for r in p] 
    def shift(p,U):
        t=[r[-U[1]:]+r[:-U[1]] for r in p]
        return t[-U[0]:]+t[:-U[0]] 
    nlm=lambda f,x,y:[map(f,x,y) for x,y in zip(x,y)]
    sense=lambda p,Z:nlm(lambda a,b:a*sensor_right if b==Z else a*(1-sensor_right),p,colors)
    move=lambda p,U:nlm(lambda x,y:p_move*x+(1-p_move)*y,shift(p,map(lambda m,l:m%l,U,[m,n])),p)
    for Z,U in zip(measurements,motions):p=norm(sense(move(p,U),Z))
    return p

if __name__ == "__main__":
    p = calculate()
    show(p)
