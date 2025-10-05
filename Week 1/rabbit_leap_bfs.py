from collections import deque

def produce_next_positions(current_state):
    layout = list(current_state)
    total = len(layout)
    empty_index = layout.index('_')
    next_positions = []
    for offset in [-1, -2, 1, 2]:
        target = empty_index + offset
        if target < 0 or target >= total:
            continue
        jumper = layout[target]
        if jumper == '_':
            continue
        if jumper == 'E' and offset < 0:
            new_layout = layout[:]
            new_layout[empty_index], new_layout[target] = new_layout[target], new_layout[empty_index]
            next_positions.append(''.join(new_layout))
        if jumper == 'W' and offset > 0:
            new_layout = layout[:]
            new_layout[empty_index], new_layout[target] = new_layout[target], new_layout[empty_index]
            next_positions.append(''.join(new_layout))
    return next_positions

def bfs_rabbit_leap():
    start_state = 'EEE_WWW'
    end_state = 'WWW_EEE'
    waiting = deque()
    waiting.append((start_state, [start_state]))
    visited = set()
    visited.add(start_state)
    while waiting:
        state, path = waiting.popleft()
        if state == end_state:
            return path
        for nxt in produce_next_positions(state):
            if nxt not in visited:
                visited.add(nxt)
                waiting.append((nxt, path + [nxt]))
    return None

bfs_result = bfs_rabbit_leap()
print("BFS Path:")
for step in bfs_result:
    print(step)
