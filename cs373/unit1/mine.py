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

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

def calculate():
    sensor_wrong = 1 - sensor_right
    p_wrong_move = (1 - p_move) / 4
    height = len(colors)
    width = len(colors[0])

    def make_prob_vector(n,m):
        alpha = n * m
        width = [1.0/alpha for _ in range(m)]
        return [width for _ in range(n)]

    def sense(p, Z):
        q = []
        for row in range(height):
            q.append([])
            for col in range(width):
                if colors[row][col] == Z:
                    q[row].append(p[row][col] * sensor_right)
                else:
                    q[row].append(p[row][col] * sensor_wrong)
        s = sum(map(sum, q))
        q = [map(lambda x: x/s, i) for i in q]
        return q

    def move(p, U):
        q = [x[:] for x in p]
        for row in range(height):
            for col in range(width):
                if U[0] == 0:
                    if U[1] == 0: # no move
                        return q
                    else:
                        s = p_wrong_move * p[(row - U[0]) % height][col]
                        s += p_wrong_move * p[row][(col + U[1]) % width] # from E
                        s += p_wrong_move * p[(row + U[0]) % height][col]
                        s += p_move * p[row][(col - U[1]) % width] # or W
                        q[row][col] = s
                else:
                    s = p_move * p[(row - U[0]) % height][col] # came from N
                    s += p_wrong_move * p[row][(col + U[1]) % width]
                    s += p_wrong_move * p[(row + U[0]) % height][col] # or S
                    s += p_wrong_move * p[row][(col - U[1]) % width]
                    q[row][col] = s
        return q

    p = make_prob_vector(height, width)

    for k in range(len(measurements)):
        p = move(p, motions[k])
        p = sense(p, measurements[k])

    #Your probability array must be printed 
    #with the following code.
    show(p)
    return p
