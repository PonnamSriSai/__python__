'''
week 4 of PDSA course

topics:
    1. introduction to graphs
        G:(V, E)
        where E subset of (V x V)
    2. Representaion of graph
        a. adjacency matrix
        b. adjacency list
    3. Graph Traversal Algos
        a. bfs
        b. dfs
    4. Application of BFS and DFS
        a. Connected Components in graph using BFS
        b. Classifying edges in directed graphs using pre and post 
           numbering i.e, tree edge, back edge, cross edge
    5. Topological Sort
    6. Longest Path in DAG
'''

import numpy as np
from week_3 import Queue

def adjacency_matrix(V : list[int],
                     E : list[tuple[int, int]],
                     directed : bool = True) -> np.ndarray:
    '''
    complexity : O(V^2)
    '''
    no_nodes = len(V)
    a_mat = np.zeros(shape = (no_nodes, no_nodes))
    
    for u, v in E:
        a_mat[u, v] = 1
        if not directed:
            a_mat[v, u] = 1
        
    return a_mat

def adjacency_list(V : list[int],
                   E : list[tuple[int, int]],
                   directed : bool = True
    ) -> dict:
    '''
    complexity: O(V + E)
    '''
    
    a_list = dict()
    for v in V:
        a_list[v] = []
        
    for u, v in E:
        a_list[u].append(v)
        if not directed:
            a_list[v].append(u)
                        
    return a_list
        
def bfs_alist(a_list : dict,
              start_vertex : int
    ) -> tuple:
    '''
    complexity: O(V + E)
    '''
    visited, parent, level, queue = {}, {}, {},Queue()
    
    for v in a_list.keys():
        visited[v] = False
        parent[v] = -1
    queue.enqueue(start_vertex)
    visited[start_vertex] = True
    level[start_vertex] = 0
    
    while not queue.is_empty():
        curr_vertex = queue.dequeue()
        for nbh in a_list[curr_vertex]:
            if not visited[nbh]:
                visited[nbh] = True
                parent[nbh] = curr_vertex
                level[nbh] = level[curr_vertex] + 1
                queue.enqueue(nbh)
                
    return visited, parent, level
            
def bfs_amat(
        a_mat : np.ndarray,
        start_vertex : int
        ) -> tuple:
    '''
    complexity: O(V^2)
    '''
    visited = {start_vertex : True}
    parent = {}
    queue = Queue()
    
    queue.enqueue(start_vertex)
    
    while not queue.is_empty():
        curr_vertex = queue.dequeue()
        for nbh, edge in enumerate(a_mat[curr_vertex]):
            if edge and nbh not in visited.keys():
                visited[nbh] = True
                parent[nbh] = curr_vertex
                queue.enqueue(nbh)
                
    return visited, parent

def dfs_alist(
        a_list : dict,
        start_vertex : int
    ) -> tuple:
    '''
    Coplexity: O(V + E)
    '''
    
    visited, pre, post, parent, tree_edges, count = {}, {}, {}, {}, set(), 0
    
    def dfs(vertex):
        nonlocal count
        visited[vertex] = True
        pre[vertex] = count
        count += 1
        for nbh in a_list[vertex]:
            if not visited.get(nbh, False):
                parent[nbh] = vertex
                tree_edges.add((vertex, nbh))
                dfs(nbh)
            
        post[vertex] = count
        count += 1
        
    dfs(start_vertex)
    
    return visited, pre, post, parent, tree_edges 

def dfs_amat(
        a_mat : list[list[int]],
        start_vertex : int
    ) -> tuple:
    '''
    Coplexity: O(V^2)
    '''
    
    visited, pre, post, parent, tree_edges, count = {}, {}, {}, {}, set(), 0
    
    def dfs(vertex):
        nonlocal count
        visited[vertex] = True
        pre[vertex] = count
        count += 1
        for nbh, edge in enumerate(a_mat[vertex]):
            if not visited.get(nbh, False) and edge:
                parent[nbh] = vertex
                tree_edges.add((vertex, nbh))
                dfs(nbh)
            
        post[vertex] = count
        count += 1
        
    dfs(start_vertex)
    
    return visited, pre, post, parent, tree_edges 

def connected_components_bfs(a_list : dict) -> tuple:
    '''
    Complexity: O(V + E)
    '''
    component = {v:-1 for v in a_list.keys()}
    component_no = 0
    
    for v in a_list.keys():
        if component[v] == -1:
            visited = bfs_alist(a_list, v)[0]
            for nbh, is_visited in visited.items():
                if is_visited:
                    component[nbh] = component_no
            component_no += 1
            
    return component_no, component

def edge_classification_alist(a_list: dict, start_vertex: int) -> dict:
    '''
    Complexity: O(V + E)
    '''
    edge_classification = dict()
    visited, pre, post, parent, tree_edges = dfs_alist(a_list, start_vertex)

    for u in a_list:
        for v in a_list[u]:
            if (u, v) in tree_edges:
                edge_classification[(u, v)] = "tree edge"
            elif pre[u] < pre[v] and post[v] < post[u]:
                edge_classification[(u, v)] = "forward edge"
            elif pre[v] < pre[u] and post[u] < post[v]:
                edge_classification[(u, v)] = "backward edge"
            else:
                edge_classification[(u, v)] = "cross edge"
    return edge_classification
                
def topological_sort_alist(a_list : dict) -> tuple:
    '''
    Complexity: O(V + E)
    '''
    indegree = {v:0 for v in a_list.keys()}
    for v in a_list.keys():
        for u in a_list.get(v):
            indegree[u] += 1
    queue = Queue()
    topological_sort = []
    path = {v:0 for v in a_list.keys()}
    for v, degree in indegree.items():
        if not degree:
            queue.enqueue(v)
    while not queue.is_empty():
        curr_vertex = queue.dequeue()
        for nbh in a_list.get(curr_vertex):
            indegree[nbh] -= 1
            if not indegree[nbh]:
                queue.enqueue(nbh)
            path[nbh] = max(path[nbh], path[curr_vertex] + 1)
        topological_sort.append(curr_vertex)
        
    if len(topological_sort) != len(a_list):
        raise ValueError("Graph is not a DAG (cycle detected)")
        
    return max(path.values()), topological_sort

def longest_path_dag_alist(a_list : dict):
    return topological_sort_alist(a_list)[0]


if __name__ == '__main__':
    
    assert np.array_equal(
                            adjacency_matrix(
                                [0, 1, 2, 3, 4],
                                [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 3), (3, 4)]
                            ),
                            np.array([
                                [0, 1, 1, 0, 0],
                                [0, 0, 0, 1, 1],
                                [0, 0, 0, 1, 1],
                                [0, 0, 0, 0, 1],
                                [0, 0, 0, 0, 0]
                            ])
    )
    
    assert adjacency_list(
            [0,1,2,3,4],
            [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 3), (3, 4)]
    ) == {0: [1, 2], 1: [3, 4], 2: [4, 3], 3: [4], 4: []}
    
    assert bfs_alist(
                {0: [1, 2], 1: [3, 4], 2: [4, 3], 3: [4], 4: []},
                0
    )[0] == {0: True, 1: True, 2: True, 3: True, 4: True}
    
    assert(bfs_amat(
               adjacency_matrix(
                   [0,1,2,3,4],
                   [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 3), (3, 4)]
               ),
               0
           )[0] == {0: True, 1: True, 2: True, 3: True, 4: True}
    )
    
    assert(
        bfs_alist(
            {0: [1, 2], 1: [3, 4], 2: [4, 3], 3: [4], 4: []},
            0
        )[:2] == ({0: True, 1: True, 2: True, 3: True, 4: True}, {0: -1, 1: 0, 2: 0, 3: 1, 4: 1})
    )
    
    assert(
        bfs_alist(
            {0: [1, 2], 1: [3, 4], 2: [4, 3], 3: [4], 4: []},
            0
        )[1:][::-1] == ({0: 0, 1: 1, 2: 1, 3: 2, 4: 2}, {0: -1, 1: 0, 2: 0, 3: 1, 4: 1})   
    )
    
    assert dfs_alist({0:[1], 1:[2], 2:[]}, 0) == (
        {0: True, 1: True, 2: True},     # visited
        {0: 0, 1: 1, 2: 2},              # pre
        {2: 3, 1: 4, 0: 5},              # post
        {1: 0, 2: 1},                    # parent
        {(0, 1), (1, 2)}                 # tree edges
    )
    
    assert dfs_alist(
            {0:[1,2], 1:[3], 2:[4], 3:[], 4:[]},
            0
        ) == (
        {0: True, 1: True, 2: True, 3: True, 4: True},
        {0: 0, 1: 1, 3: 2, 2: 5, 4: 6},   # pre
        {3: 3, 1: 4, 4: 7, 2: 8, 0: 9},   # post
        {1: 0, 3: 1, 2: 0, 4: 2},
        {(0, 1), (1, 3), (0, 2), (2, 4)}
    )

    assert dfs_amat([
                [0,1,0],
                [0,0,1],
                [0,0,0]
            ],
            0
        ) == (
        {0: True, 1: True, 2: True},
        {0: 0, 1: 1, 2: 2},
        {2: 3, 1: 4, 0: 5},
        {1: 0, 2: 1},
        {(0, 1), (1, 2)}
    )
    
    assert dfs_amat([
                [0,1,1,0,0],
                [0,0,0,1,0],
                [0,0,0,0,1],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ], 
            0
        ) == (
        {0: True, 1: True, 2: True, 3: True, 4: True},
        {0: 0, 1: 1, 3: 2, 2: 5, 4: 6},   # pre
        {3: 3, 1: 4, 4: 7, 2: 8, 0: 9},   # post
        {1: 0, 3: 1, 2: 0, 4: 2},
        {(0, 1), (1, 3), (0, 2), (2, 4)}
    )
            
    assert connected_components_bfs({
                    0: [1],
                    1: [0, 2],
                    2: [1],
                    3: [4],
                    4: [3],
                    5: []
                }) == (
        3,
        {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2}
    )
                    
    # Case 1: Simple tree edges only
    assert edge_classification_alist(
        {0: [1, 2], 1: [], 2: []}, 0
    ) == {
        (0, 1): "tree edge",
        (0, 2): "tree edge"
    }
    
    # Case 2: Tree + Backward edge
    assert edge_classification_alist(
        {0: [1], 1: [2], 2: [0]}, 0
    ) == {
        (0, 1): "tree edge",
        (1, 2): "tree edge",
        (2, 0): "backward edge"
    }
    
    # Case 3: Tree + Cross edge
    assert edge_classification_alist(
        {0: [1, 2], 1: [2], 2: []}, 0
    ) == {
        (0, 1): "tree edge",
        (0, 2): "forward edge",
        (1, 2): "tree edge"
    }
    
    # Case 4: Forward edge explicitly
    assert edge_classification_alist(
        {0: [1, 2], 1: [3], 2: [], 3: []}, 0
    ) == {
        (0, 1): "tree edge",
        (0, 2): "tree edge",
        (1, 3): "tree edge"
    }
        
    # simple chain
    assert topological_sort_alist({0:[1], 1:[2], 2:[]})[1] == [0,1,2]
    
    # diamond graph (multiple valid topological sorts)
    result = topological_sort_alist({0:[1,2], 1:[3], 2:[3], 3:[]})[1]
    assert result in ([0,1,2,3], [0,2,1,3])
    
    # disconnected DAG
    result = topological_sort_alist({0:[1], 1:[], 2:[3], 3:[]})[1]
    assert result in ([0,1,2,3], [2,3,0,1], [0, 2, 1, 3])
    
    # cycle detection
    try:
        topological_sort_alist({0:[1], 1:[2], 2:[0]})
        assert False, "Should have raised ValueError for cycle"
    except ValueError:
        pass
    
    # DAG 1: Simple chain 0 -> 1 -> 2 -> 3
    assert longest_path_dag_alist({
        0: [1],
        1: [2],
        2: [3],
        3: []
    }) == 3    # longest path = 0→1→2→3 (length 3 edges)
    
    # DAG 2: Diamond shape 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
    assert longest_path_dag_alist({
        0: [1, 2],
        1: [3],
        2: [3],
        3: []
    }) == 2    # longest path = 0→1→3 or 0→2→3
    
    # DAG 3: Two independent chains
    assert longest_path_dag_alist({
        0: [1],
        1: [],
        2: [3, 4],
        3: [],
        4: []
    }) == 1    # longest path = 2→4 or 2→3
    
    # DAG 4: Single vertex, no edges
    assert longest_path_dag_alist({
        0: []
    }) == 0    # no edges, longest path length = 0
    
    # DAG 5: Complex graph
    assert longest_path_dag_alist({
        5: [2, 0],
        4: [0, 1],
        2: [3],
        3: [1],
        0: [],
        1: []
    }) == 3    # longest path = 5→2→3→1
