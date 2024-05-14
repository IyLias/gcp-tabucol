from collections import deque
from random import randrange
import networkx as nx 


def tabucol(graph,k,tabu_size=7,reps=100,max_iterations=10000):
    
    """ parameter 

        graph: networkx graph  
        k : number of colors using 
        tabu_size: size of tabu list 
        reps: number of iterations searching neighbor solution
        max_iterations: maximum iterations of tabucol

        return 

        solution: solution list applied tabucol
    """
    N = graph.order()
    colors = list(range(k))
    
    # Tabu List 
    tabu = deque() 
    iterations = 0
    
    solution = dict()
    for i in range(N):
        solution[i] = colors[randrange(0, len(colors))]

    
    while iterations < max_iterations:
        
        conflicting_nodes = set()
        conflicts = 0
        for node in graph.nodes():
            for neighbor in graph.neighbors(node):
                if solution[node] == solution[neighbor]:
                    conflicting_nodes.add(node)
                    conflicting_nodes.add(neighbor)
                    conflicts += 1
        
        conflicting_nodes = list(conflicting_nodes)
        # Exit Condition
        if conflicts == 0:
            break

        
        # Exploring Neighbor solutions
        new_solution = None
        for r in range(reps):
            node = conflicting_nodes[randrange(0,len(conflicting_nodes))]

            new_color = colors[randrange(0,len(colors))]
            while solution[node] == new_color:
                new_color = colors[randrange(0,len(colors))]

            new_conflicts = 0
            for node in graph.nodes():
                for neighbor in graph.neighbors(node):
                    if solution[node] == solution[neighbor]:
                        new_conflicts += 1

            # If found a better solution, 
            if new_conflicts < conflicts:


            




