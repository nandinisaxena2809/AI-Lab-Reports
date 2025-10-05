import heapq,time
from board import initial_board,is_goal,neighbors
from heuristics import h_manhattan_div2_ceil,h_marbles_minus_one
def best_first_search(heuristic):
    start=initial_board()
    pq=[(heuristic(start),start)]
    visited=set([start])
    parent={}
    nodes_expanded=0
    start_time=time.time()
    while pq:
        h,state=heapq.heappop(pq)
        nodes_expanded+=1
        if is_goal(state):
            path=[]
            cur=state
            while cur in parent:
                path.append(cur)
                cur=parent[cur]
            path.append(cur)
            path.reverse()
            return {'name':'Greedy','heuristic':heuristic.__name__,'time':time.time()-start_time,'nodes':nodes_expanded,'length':len(path)-1}
        for nb in neighbors(state):
            if nb not in visited:
                visited.add(nb)
                parent[nb]=state
                heapq.heappush(pq,(heuristic(nb),nb))
    return {'name':'Greedy','heuristic':heuristic.__name__,'time':time.time()-start_time,'nodes':nodes_expanded,'length':None}
if __name__=='__main__':
    print(best_first_search(h_manhattan_div2_ceil))
    print(best_first_search(h_marbles_minus_one))
