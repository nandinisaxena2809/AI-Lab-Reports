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

def dfs_rabbit_leap():
    start_state = 'EEE_WWW'
    end_state = 'WWW_EEE'
    stack = [(start_state, [start_state])]
    visited = set()
    visited.add(start_state)
    while stack:
        state, path = stack.pop()
        if state == end_state:
            return path
        for nxt in produce_next_positions(state):
            if nxt not in visited:
                visited.add(nxt)
                stack.append((nxt, path + [nxt]))
    return None

dfs_result = dfs_rabbit_leap()
print("DFS Path:")
for step in dfs_result:
    print(step)
