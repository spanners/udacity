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
    def sense(p, Z):
        q = [[vv * (sensor_right if cc==Z else 1-sensor_right) 
                for vv,cc in zip(v,c)] for v,c in zip(p,colors)]
        return [[vv/sum(map(sum,q)) for vv in v] for v in q]

    def move(p, U):
        return [[p_move * p[(i-U[0])%len(p)][(j-U[1])%len(p[0])] + (1-p_move) * p[i][j] 
                for j in range(len(p[0]))] for i in range(len(p))]

    p = [[(1.0 / (len(colors) * len(colors[0]))) for _ in colors[0]] for _ in colors]

    for k in range(len(measurements)):
        p = move(p, motions[k])
        p = sense(p, measurements[k])

    return p

if __name__ == "__main__":
    p = calculate()
    show(p)
