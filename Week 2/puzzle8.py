from collections import deque

GOAL = ((1,2,3),(4,5,6),(7,8,0))

# ---------- Utility functions ----------
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def actions(state):
    i, j = find_blank(state)
    moves = []
    if i > 0: moves.append("UP")
    if i < 2: moves.append("DOWN")
    if j > 0: moves.append("LEFT")
    if j < 2: moves.append("RIGHT")
    return moves

def result(state, action):
    i, j = find_blank(state)
    new = [list(row) for row in state]  # copy
    if action == "UP": ni, nj = i-1, j
    if action == "DOWN": ni, nj = i+1, j
    if action == "LEFT": ni, nj = i, j-1
    if action == "RIGHT": ni, nj = i, j+1
    new[i][j], new[ni][nj] = new[ni][nj], new[i][j]
    return tuple(tuple(row) for row in new)

# Node structure = (state, parent, action, depth)
def make_node(state, parent=None, action=None, depth=0):
    return (state, parent, action, depth)

def backtrack(node):
    path = []
    while node:
        path.append(node[0])
        node = node[1]
    return list(reversed(path))

# ---------- Graph Search ----------
def bfs(start):
    frontier = deque([make_node(start)])
    explored = set()
    frontier_states = {start}
    while frontier:
        node = frontier.popleft()
        state = node[0]
        frontier_states.remove(state)
        if state == GOAL:
            return backtrack(node)
        explored.add(state)
        for act in actions(state):
            child_state = result(state, act)
            if child_state not in explored and child_state not in frontier_states:
                frontier.append(make_node(child_state, node, act, node[3]+1))
                frontier_states.add(child_state)
    return None

def dfs(start, limit=20):
    stack = [make_node(start)]
    explored = set()
    while stack:
        node = stack.pop()
        state = node[0]
        if state == GOAL:
            return backtrack(node)
        explored.add(state)
        if node[3] < limit:
            for act in actions(state):
                child_state = result(state, act)
                if child_state not in explored:
                    stack.append(make_node(child_state, node, act, node[3]+1))
    return None

def ids(start):
    depth = 0
    while True:
        path = dfs(start, limit=depth)
        if path: return path
        depth += 1

# ---------- Example ----------
start = ((2,8,3),(1,6,4),(7,0,5))  
solution = bfs(start)
if solution is None:
    print("No solution found.")
else:
    print("Solution length:", len(solution)-1)
    for s in solution:
        for row in s:
            print(row)
        print()
