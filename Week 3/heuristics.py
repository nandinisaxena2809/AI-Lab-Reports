from board import count_marbles,total_manhattan_to_center
import math
def h_marbles_minus_one(state):
    return count_marbles(state)-1
def h_manhattan_div2_ceil(state):
    return math.ceil(total_manhattan_to_center(state)/2)
