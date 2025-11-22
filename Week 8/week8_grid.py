import numpy as np
import random

CONVERGENCE_LIMIT = 0.05
GAMMA = 0.99
TRANSITION_NOISE = 0.1  

grid_states = [(r, c) for r in range(3) for c in range(4)]

state_reward = {}
for s in grid_states:
    if s == (1, 3):
        state_reward[s] = -1
    elif s == (2, 3):
        state_reward[s] = 1
    else:
        state_reward[s] = -0.04

state_actions = {
    (0, 0): ('D', 'R'),
    (0, 1): ('D', 'R', 'L'),
    (0, 2): ('D', 'L', 'R'),
    (0, 3): ('D', 'L'),
    (1, 2): ('U', 'D', 'L', 'R'),
    (1, 0): ('D', 'U', 'R'),
    (2, 0): ('U', 'R'),
    (2, 1): ('U', 'L', 'R'),
    (2, 2): ('U', 'L', 'R'),
}

policy = {s: np.random.choice(state_actions[s]) for s in state_actions}

state_value = {}
for s in grid_states:
    if s in state_actions:
        state_value[s] = 0
    if s == (1, 3):
        state_value[s] = -1
    if s == (2, 3):
        state_value[s] = 1
    if s == (1, 1):
        state_value[s] = 0

iteration = 0
while True:
    max_delta = 0

    for s in grid_states:
        if s not in policy:
            continue

        previous_value = state_value[s]
        highest_estimate = -1e6

        for act in state_actions[s]:

            if act == 'U':
                main_next = (s[0] - 1, s[1])
            elif act == 'D':
                main_next = (s[0] + 1, s[1])
            elif act == 'L':
                main_next = (s[0], s[1] - 1)
            elif act == 'R':
                main_next = (s[0], s[1] + 1)

            alt = np.random.choice([a for a in state_actions[s] if a != act])
            rng = random.randint(0, 100)

            if 80 < rng <= 90:
                alt_map = {'U':'L','D':'R','L':'D','R':'U'}
                alt = alt_map[alt]
            elif rng > 90:
                alt_map = {'U':'R','D':'L','L':'U','R':'D'}
                alt = alt_map[alt]

            if alt == 'U':
                noisy_next = (s[0] - 1, s[1])
            elif alt == 'D':
                noisy_next = (s[0] + 1, s[1])
            elif alt == 'L':
                noisy_next = (s[0], s[1] - 1)
            elif alt == 'R':
                noisy_next = (s[0], s[1] + 1)

            if 0 <= noisy_next[0] < 3 and 0 <= noisy_next[1] < 4:
                est_value = state_reward[s] + GAMMA * (
                    (1 - TRANSITION_NOISE) * state_value.get(main_next, state_value[s]) +
                    TRANSITION_NOISE * state_value.get(noisy_next, state_value[s])
                )

                if est_value > highest_estimate:
                    highest_estimate = est_value
                    policy[s] = act

        state_value[s] = highest_estimate
        max_delta = max(max_delta, abs(previous_value - state_value[s]))

    if max_delta < CONVERGENCE_LIMIT:
        break

    iteration += 1


print(f"Iterations needed: {iteration}\n")
for s, v in state_value.items():
    print(f"State {s}: Value = {v}")


