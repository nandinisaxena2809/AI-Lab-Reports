from collections import deque

def validate_side(m_side, c_side):
    if m_side < 0 or c_side < 0 or m_side > 3 or c_side > 3:
        return False
    if m_side > 0 and m_side < c_side:
        return False
    return True

def generate_next_positions(current_state):
    a_m, a_c, b_m, b_c, vessel = current_state
    shifts = [(1,0),(2,0),(0,1),(0,2),(1,1)]
    outcomes = []
    for m_shift, c_shift in shifts:
        if vessel == 'A':
            new_a_m = a_m - m_shift
            new_a_c = a_c - c_shift
            new_b_m = b_m + m_shift
            new_b_c = b_c + c_shift
            new_vessel = 'B'
        else:
            new_a_m = a_m + m_shift
            new_a_c = a_c + c_shift
            new_b_m = b_m - m_shift
            new_b_c = b_c - c_shift
            new_vessel = 'A'
        if validate_side(new_a_m, new_a_c) and validate_side(new_b_m, new_b_c):
            outcomes.append((new_a_m, new_a_c, new_b_m, new_b_c, new_vessel))
    return outcomes

def bfs_solution():
    start_state = (3,3,0,0,'A')
    end_state = (0,0,3,3,'B')
    waiting = deque()
    waiting.append((start_state, [start_state]))
    visited = set()
    visited.add(start_state)
    while waiting:
        state, path = waiting.popleft()
        if state == end_state:
            return path
        for next_state in generate_next_positions(state):
            if next_state not in visited:
                visited.add(next_state)
                waiting.append((next_state, path + [next_state]))
    return None

bfs_path = bfs_solution()
print("BFS Path:")
for p in bfs_path:
    print(p)
