from ucs import uniform_cost_search
from greedy import best_first_search
from astar import astar
from heuristics import h_manhattan_div2_ceil,h_marbles_minus_one
import json,time
def run_all():
    results=[]
    results.append(uniform_cost_search())
    results.append(best_first_search(h_manhattan_div2_ceil))
    results.append(best_first_search(h_marbles_minus_one))
    results.append(astar(h_manhattan_div2_ceil))
    results.append(astar(h_marbles_minus_one))
    print(json.dumps(results,indent=2))
if __name__=='__main__':
    run_all()
