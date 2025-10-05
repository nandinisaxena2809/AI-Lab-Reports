import heapq, time
from board import initial_board, is_goal, neighbors
def uniform_cost_search():
    start=initial_board()
    start_g=0
    pq=[(start_g,start)]
    came_g={start:0}
    parent={}
    nodes_expanded=0
    start_time=time.time()
    while pq:
        g,state=heapq.heappop(pq)
        if g!=came_g[state]:
            continue
        nodes_expanded+=1
        if is_goal(state):
            path=[]
            cur=state
            while cur in parent:
                path.append(cur)
                cur=parent[cur]
            path.append(cur)
            path.reverse()
            return {'name':'UCS','time':time.time()-start_time,'nodes':nodes_expanded,'cost':g,'length':len(path)-1}
        for nb in neighbors(state):
            ng=g+1
            if nb not in came_g or ng<came_g[nb]:
                came_g[nb]=ng
                parent[nb]=state
                heapq.heappush(pq,(ng,nb))
    return {'name':'UCS','time':time.time()-start_time,'nodes':nodes_expanded,'cost':None,'length':None}
if __name__=='__main__':
    print(uniform_cost_search())

