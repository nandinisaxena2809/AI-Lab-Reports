import numpy as np
from math import exp, factorial
from copy import deepcopy
import time


MAX_BIKE_CAPACITY = 20
MAX_BIKE_MOVE = 5
RENTAL_INCOME = 10
BIKE_MOVE_COST = 2
SECOND_PARKING_FEE = 4
PARKING_LIMIT = 10

EXPECTED_DAILY_REQUESTS = [3, 4]  # location1, location2
EXPECTED_DAILY_RETURNS = [3, 2]   # location1, location2

DISCOUNT_FACTOR = 0.9
CONVERGENCE_THRESHOLD = 1e-3
POISSON_MAX = 11  # Cutoff for Poisson distribution PMF


def poisson_probability(k, lam):
    
    return exp(-lam) * lam**k / factorial(k)


def generate_poisson_distribution(lam):
  
    pmf_list = [poisson_probability(i, lam) for i in range(POISSON_MAX)]
    tail = 1 - sum(pmf_list)
    pmf_list[-1] += tail
    return pmf_list



poisson_rent_cache = [generate_poisson_distribution(lam) for lam in EXPECTED_DAILY_REQUESTS]
poisson_return_cache = [generate_poisson_distribution(lam) for lam in EXPECTED_DAILY_RETURNS]


all_states = [(b1, b2) for b1 in range(MAX_BIKE_CAPACITY + 1) for b2 in range(MAX_BIKE_CAPACITY + 1)]


def possible_actions(state):

    bikes_loc1, bikes_loc2 = state
    feasible = []
    for move in range(-MAX_BIKE_MOVE, MAX_BIKE_MOVE + 1):
        after_move_loc1 = bikes_loc1 - move
        after_move_loc2 = bikes_loc2 + move
        if 0 <= after_move_loc1 <= MAX_BIKE_CAPACITY and 0 <= after_move_loc2 <= MAX_BIKE_CAPACITY:
            feasible.append(move)
    return feasible


def calculate_move_cost(action):
    
    if action <= 0:
        return abs(action) * BIKE_MOVE_COST
    else:
        return max(0, action - 1) * BIKE_MOVE_COST


def calculate_parking_fee(bike_count):
  
    return SECOND_PARKING_FEE if bike_count > PARKING_LIMIT else 0



transitions_dict = {}

print("Starting transition precomputation...")
start_time = time.time()
for idx, current_state in enumerate(all_states):
    if (idx + 1) % 100 == 0:
        print(f"Processed {idx + 1}/{len(all_states)} states ({time.time() - start_time:.1f} seconds elapsed)")
    bikes_loc1, bikes_loc2 = current_state
    for action_move in possible_actions(current_state):

        bikes_after_move_loc1 = bikes_loc1 - action_move
        bikes_after_move_loc2 = bikes_loc2 + action_move

        cost_move = calculate_move_cost(action_move)
        cost_parking = calculate_parking_fee(bikes_after_move_loc1) + calculate_parking_fee(bikes_after_move_loc2)

        state_action_outcomes = {}

        for rent_req1 in range(POISSON_MAX):
            prob_rent1 = poisson_rent_cache[0][rent_req1]
            actual_rent1 = min(rent_req1, bikes_after_move_loc1)
            income_loc1 = actual_rent1 * RENTAL_INCOME

            for rent_req2 in range(POISSON_MAX):
                prob_rent2 = poisson_rent_cache[1][rent_req2]
                actual_rent2 = min(rent_req2, bikes_after_move_loc2)
                income_loc2 = actual_rent2 * RENTAL_INCOME

                prob_rentals = prob_rent1 * prob_rent2

                bikes_after_rent_loc1 = bikes_after_move_loc1 - actual_rent1
                bikes_after_rent_loc2 = bikes_after_move_loc2 - actual_rent2

                for ret1 in range(POISSON_MAX):
                    prob_return1 = poisson_return_cache[0][ret1]
                    new_bikes_loc1 = min(bikes_after_rent_loc1 + ret1, MAX_BIKE_CAPACITY)

                    for ret2 in range(POISSON_MAX):
                        prob_return2 = poisson_return_cache[1][ret2]
                        new_bikes_loc2 = min(bikes_after_rent_loc2 + ret2, MAX_BIKE_CAPACITY)

                        total_prob = prob_rentals * prob_return1 * prob_return2
                        total_reward = income_loc1 + income_loc2 - cost_move - cost_parking

                        next_state = (new_bikes_loc1, new_bikes_loc2)
                        if next_state not in state_action_outcomes:
                            state_action_outcomes[next_state] = [0.0, 0.0]
                        state_action_outcomes[next_state][0] += total_prob
                        state_action_outcomes[next_state][1] += total_prob * total_reward

        
        transitions_dict[(current_state, action_move)] = []
        for next_st, (prob_sum, reward_sum) in state_action_outcomes.items():
            expected_reward = reward_sum / prob_sum
            transitions_dict[(current_state, action_move)].append((prob_sum, next_st, expected_reward))

print(f"Transition precomputation completed in {time.time() - start_time:.1f} seconds.\n")



current_policy = {state: 0 for state in all_states}


def evaluate_policy(policy, value_init=None):
 
    state_values = {state: 0.0 for state in all_states} if value_init is None else deepcopy(value_init)
    while True:
        max_diff = 0
        for state in all_states:
            action = policy[state]
            value = 0
            for (prob, next_state, reward) in transitions_dict[(state, action)]:
                value += prob * (reward + DISCOUNT_FACTOR * state_values[next_state])
            max_diff = max(max_diff, abs(state_values[state] - value))
            state_values[state] = value
        if max_diff < CONVERGENCE_THRESHOLD:
            break
    return state_values


def improve_policy(value_func, old_policy):
   
    policy_stable_flag = True
    updated_policy = {}
    for state in all_states:
        action_values = {}
        for action in possible_actions(state):
            val = 0
            for (prob, next_state, reward) in transitions_dict[(state, action)]:
                val += prob * (reward + DISCOUNT_FACTOR * value_func[next_state])
            action_values[action] = val
        best_action = max(action_values, key=action_values.get)
        updated_policy[state] = best_action
        if best_action != old_policy[state]:
            policy_stable_flag = False
    return updated_policy, policy_stable_flag


print("Starting policy iteration...")
values = None
iteration_count = 0
while True:
    iteration_count += 1
    values = evaluate_policy(current_policy, value_init=values)
    current_policy, stable = improve_policy(values, current_policy)
    print(f"Policy iteration {iteration_count}: policy stable = {stable}")
    if stable or iteration_count >= 50:
        break

print("\nPolicy iteration completed.\n")

print("Sample optimal policy (rows: bikes at location1 = 0..10; columns: bikes at location2 = 0..20):")
for b1_count in range(11):
    policy_row = []
    for b2_count in range(MAX_BIKE_CAPACITY + 1):
        policy_row.append(f"{current_policy[(b1_count, b2_count)]:3d}")
    print(f"{b1_count:2d}: " + " ".join(policy_row))

print(f"\nValue at initial state (10 bikes loc1, 10 bikes loc2): {values[(10,10)]:.2f}")
