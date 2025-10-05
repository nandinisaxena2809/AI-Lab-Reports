from copy import deepcopy
def initial_board():
    B=[[-1,-1,1,1,1,-1,-1],[-1,-1,1,1,1,-1,-1],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[-1,-1,1,1,1,-1,-1],[-1,-1,1,1,1,-1,-1]]
    return tuple(tuple(row) for row in B)
def is_goal(state):
    c=0
    for r in range(7):
        for s in range(7):
            if state[r][s]==1:
                c+=1
    return c==1 and state[3][3]==1
def neighbors(state):
    dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    res=[]
    for r in range(7):
        for c in range(7):
            if state[r][c]==1:
                for dr,dc in dirs:
                    r1=r+dr
                    c1=c+dc
                    r2=r+2*dr
                    c2=c+2*dc
                    if 0<=r2<7 and 0<=c2<7 and 0<=r1<7 and 0<=c1<7:
                        if state[r1][c1]==1 and state[r2][c2]==0:
                            new=[list(row) for row in state]
                            new[r][c]=0
                            new[r1][c1]=0
                            new[r2][c2]=1
                            res.append(tuple(tuple(row) for row in new))
    return res
def count_marbles(state):
    return sum(1 for r in range(7) for c in range(7) if state[r][c]==1)
def total_manhattan_to_center(state):
    s=0
    for r in range(7):
        for c in range(7):
            if state[r][c]==1:
                s+=abs(r-3)+abs(c-3)
    return s
