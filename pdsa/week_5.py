'''
week-5 of PDSA

topics:
    1. representation of weighted graphs
        a. adjacency matrix
        b. adjacency list
    2. Shortest Path
        a. Single source shortest path algorithm
            i. Dijkstra's Algorithm
            ii. Bellman Ford algorithm
        b. All pair of shortest path
            i. Floyd-Warshall algorithm
    3. Spanning Tree
    4. Minimum Cost Spanning Tree(MCST)
        a. Prim's Algorithm
        b. Kruskal's Algorithm
        
programming assignments:
    1. 
'''

import numpy as np

def WMat(
        V : set[int],
        E : list[tuple[int, int, int]]
    ) -> np.ndarray:
    '''
    Complexity: O(V^2)
    '''
    no_vertices = len(V)
    Wmat = np.zeros(shape = (no_vertices, no_vertices, 2))
    
    for u, v, w in E:
        Wmat[u, v, 0] = 1
        Wmat[u, v, 1] = w
        
    return Wmat

def WList(
        V : set[int],
        E : list[tuple[int, int, int]]
    ) -> dict:
    '''
    Complexity: O(V + E)
    '''
    Wlist = {v:[] for v in V}
    
    for u, v, w in E:
        Wlist[u].append((v, w))
        
    return Wlist

def dijkstra_wlist(Wlist : dict, start_vertex : int) -> tuple:
    '''
    Single-source shortest path
    Weighted graph
    Non-negative weights
    Greedy algorithm
    Optimal substructure
    Can handle disconnected graphs
    
    Complexity: O(V^2)
    '''
    visited, distance, parent = ({v:False for v in Wlist.keys()},
                                 {v:float('inf') for v in Wlist.keys()},
                                 {v:-1 for v in Wlist.keys()})
        
    distance[start_vertex], parent[start_vertex] = 0, start_vertex
    
    for _ in range(len(Wlist)):
        unvisited = [v for v in Wlist if not visited[v]]  
        vertex = min(unvisited, key=lambda v: distance[v])
        
        if not unvisited:
            break

        for nbh, w in Wlist[vertex]:
            if distance[nbh] > distance[vertex] + w:
                distance[nbh] = distance[vertex] + w
                parent[nbh] = vertex
                
        visited[vertex] = True
                
    return distance, parent
    
def dijkstra_wmat(Wmat : np.ndarray, start_vertex : int) -> tuple:
    '''
    Complexity: O(V^2)
    '''
    no_vertices = Wmat.shape[0]
    visited, distance, parent = ({v:False for v in range(no_vertices)},
                                 {v:float('inf') for v in range(no_vertices)},
                                 {v:-1 for v in range(no_vertices)})
        
    distance[start_vertex], parent[start_vertex] = 0, start_vertex
    
    for _ in range(no_vertices):
        unvisited = [v for v in range(no_vertices) if not visited[v]]  
        vertex = min(unvisited, key=lambda v: distance[v])
        
        if not unvisited:
            break

        for nbh in range(no_vertices):
            edge, w = Wmat[vertex, nbh]
            if edge and distance[nbh] > distance[vertex] + w:
                distance[nbh] = distance[vertex] + w
                parent[nbh] = vertex
                
        visited[vertex] = True
                
    return distance, parent

def bellman_ford_wlist(Wlist : dict, start_vertex : int) -> dict:
    '''
    Single-source shortest path
    dynamic programming based algorithm
    It can handle graphs with negative edge weights
    It can detect negative cycles
    It can handle disconnected graphs
    
    Complexity: O(V^3)
    '''
    no_vertices = len(Wlist)
    distance = {v:float('inf') for v in Wlist.keys()}
    parent = {v:-1 for v in Wlist.keys()}
    
    distance[start_vertex], parent[start_vertex] = 0, start_vertex
    
    for _ in range(no_vertices - 1):
        for u in Wlist.keys():
            for v, w in Wlist[u]:
                if distance[u] != float('inf') and distance[v] > distance[u] + w:
                    distance[v] = distance[u] + w
                    parent[v] = u
                    
    return distance, parent         
                
def bellman_ford_wmat(Wmat : np.ndarray, start_vertex : int) -> dict:
    '''
    Single-source shortest path
    dynamic programming based algorithm
    It can handle graphs with negative edge weights
    It can detect negative cycles
    It can handle disconnected graphs
    
    Complexity: O(V^3)
    '''
    no_vertices = Wmat.shape()[0]
    distance = {v:float('inf') for v in range(no_vertices)}
    parent = {v:-1 for v in range(no_vertices)}
    
    distance[start_vertex], parent[start_vertex] = 0, start_vertex
    
    for _ in range(no_vertices - 1):
        for u in range(no_vertices):
            for v, tup in enumerate(Wmat[u]):
                edge, w = tup
                if edge and distance[u] != float('inf') and distance[v] > distance[u] + w:
                    distance[v] = distance[u] + w
                    parent[v] = u
                    
    return distance, parent         

if __name__ == '__main__':

    # --- Test Cases for WMat ---
    V = {0, 1, 2, 3}
    E = [(0, 1, 5), (0, 2, 3), (1, 3, 7), (2, 3, 1)]
    
    Wmat = WMat(V, E)
    
    # Shape check
    assert Wmat.shape == (4, 4, 2)
    
    # Edge existence and weight checks
    assert (Wmat[0, 1, 0], Wmat[0, 1, 1]) == (1, 5)
    assert (Wmat[0, 2, 0], Wmat[0, 2, 1]) == (1, 3)
    assert (Wmat[1, 3, 0], Wmat[1, 3, 1]) == (1, 7)
    assert (Wmat[2, 3, 0], Wmat[2, 3, 1]) == (1, 1)
    
    # No edge case
    assert (Wmat[1, 2, 0], Wmat[1, 2, 1]) == (0, 0)
    
    # --- Test Cases for WList ---
    Wlist = WList(V, E)
    
    # Basic structure check
    assert set(Wlist.keys()) == V
    
    # Edge existence
    assert Wlist[0] == [(1, 5), (2, 3)]
    assert Wlist[1] == [(3, 7)]
    assert Wlist[2] == [(3, 1)]
    assert Wlist[3] == []
    
    # Edge weight correctness
    assert (1, 5) in Wlist[0]
    assert (3, 7) in Wlist[1]
    assert (3, 1) in Wlist[2]
    Wlist = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: []
    }
    
    dist, parent = dijkstra_wlist(Wlist, 0)
    
    assert dist == {0: 0, 1: 3, 2: 1, 3: 4}
    assert parent == {0: 0, 1: 2, 2: 0, 3: 1}
    V = {0, 1, 2, 3}
    E = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)]
    Wmat = WMat(V, E)

    distance, parent = dijkstra_wmat(Wmat, 0)
    expected_distance = {0: 0, 1: 1, 2: 3, 3: 6}
    expected_parent = {0: 0, 1: 0, 2: 1, 3: 2}
    
    assert (distance, parent) == (expected_distance, expected_parent)
    
    


