import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from random import randrange

import time
import wandb
from torch.utils.tensorboard import SummaryWriter

import math
from util import readDIMACS_graph

class GCP_Solver:

    def __init__(self, is_read_file, graph_path, graph_type, node, prob, k, is_track, render_mode, algorithm):
        
        self.graph_type = graph_type
        
        if is_read_file:
            self.graph = readDIMACS_graph(graph_path)
        else:
            self.graph = self.generate_graph(graph_type,node, prob)
        
        self.N = node
        self.p = prob
        self.k = k
        
        self.is_track = False
        self.algorithm = algorithm
        
        colors = list(range(k))
        
        # Initialize solution with random colors
        self.solution = np.random.randint(0,self.k, size=self.N, dtype=np.int32)
        

        assert render_mode is not None, "render mode should be designated"
        self.render_mode = render_mode
        
        # render setting 
        self.color_map = None
        self.layout = nx.spring_layout(self.graph,k=0.1)
        self.fig, self.ax = plt.subplots(figsize=(10,10))
        plt.ion()
    
        # wandb setting
        if self.is_track == True:
            print("is_track True")
            run_name = self.set_run_name(graph_type, self.N, prob, k)
            wandb.init(
                project="GCP-Heuristics",

                config={
                    "algorithm": "tabucol",
                    "reps": 100,
                    "max_iterations": 10000,
                    "alpha": 0.6
                },
                sync_tensorboard=True,
                name=run_name,
                monitor_gym=True,
                save_code=True
            )

            self.writer = SummaryWriter(f"runs/{run_name}")

    
    def generate_graph(self,graph_type, nodes, prob):
        graph = None

        if graph_type == 0:
            graph = nx.gnp_random_graph(nodes, prob)
        elif graph_type == 1:
            graph = nx.empty_graph(n=nodes)
        elif graph_type == 2:
            graph = nx.complete_graph(n=nodes)
        elif graph_type == 3:
            graph = nx.petersen_graph()
        elif graph_type == 4:
            graph = nx.cycle_graph(n=nodes)
        

        return graph


    
    def set_run_name(self,graph_type, nodes, prob, ncolors): 
    
        run_name = f"{int(time.time())}"
        #if args.random_graph == True:

        # DSJCn.x(random graph: Erdos-Renyi model) 
        if graph_type == 0:
            run_name = f"G({nodes},{prob})k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 1:
            run_name = f"O_{nodes}__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 2:
            run_name = f"K_{nodes}__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 3:
            run_name = f"Petersen__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 4:
            run_name = f"flat__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 5:
            run_name = f"le450__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 6:
            n = int(math.sqrt(nodes))
            run_name = f"queen{n}_{n}__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 7:
            run_name = f"games120__k{ncolors}__{self.algorithm}__{int(time.time())}"
        elif graph_type == 8:
            run_name = f"myciel{nodes}__k{ncolors}__{self.algorithm}__{int(time.time())}"
        

        print(run_name)
        return run_name




    def render(self,solution):

        def is_in_ipython():
            try:
                __IPYTHON__
                return True
            except NameError:
                return False

        if is_in_ipython():
            from IPython.display import clear_output
            # clear_output(wait=True)


        if self.color_map is None:
            self.color_map = {
                    j:f"#{''.join([random.choice('0123456789ABCDEF') for i in range(6)])}" for j in range(self.k)
            }

        if self.layout is None:
            self.layout = nx.spring_layout(self.graph)


        #fig, ax = plt.subplots(figsize=(10, 10))
        #fig.tight_layout()
        #ax.axis("off")

        node_colors = [self.color_map[node] for node in solution]

        edge_colors = [
            "#ff0000" if solution[x] == solution[y] else "#000000"
            for x, y in nx.edges(self.graph)
        ]
        alphas = [
            1.0 if solution[x] == solution[y] else 0.1
            for x, y in nx.edges(self.graph)
        ]

        self.ax.clear()
        self.ax.axis('off')

        #plt.cla()
        nx.draw_networkx_nodes(self.graph, self.layout, node_color=node_colors)
        nx.draw_networkx_labels(self.graph, self.layout)
        nx.draw_networkx_edges(
            self.graph, self.layout, edge_color=edge_colors, alpha=alphas
        )


        # Display these info as text on the plot
        n_conflicts = self.count_conflicts(self.graph, solution)
        n_colors_used = len(np.unique(self.solution))

        info_text = f"Graph order: {self.graph.order()}\nGraph size: {self.graph.size()} \n\nNumber of Colors: {n_colors_used} \nConflicts: {n_conflicts}"
        self.ax.text(0.01, 0.99, info_text, transform=self.ax.transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.1)


        if self.render_mode == "file":

            image_from_plot = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
            image_from_plot = image_from_plot.reshape(
                self.fig.canvas.get_width_height()[::-1] + (3,)
            )

            img = Image.fromarray(image_from_plot)
            print("saving", f"{self.base_filename}{self.render_iter}.png")
            img.save(f"{self.base_filename}{self.render_iter}.png")
            self.render_iter += 1
            plt.close()

        elif self.render_mode == "human" or self.render_mode == "rgb_array":
            plt.show()

            # if capture_video, should return pixel array
            if self.render_mode == "rgb_array":
                self.fig.canvas.draw()
                image_from_plot = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
                image_from_plot = image_from_plot.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
                return image_from_plot



    def tabucol(self,graph,k,tabu_size=7,reps=100,max_iterations=10000, alpha=0.6):

        """
        function tabucol() implements tabucol algorithm

            parameter

                graph: networkx graph
                k : number of colors using
                tabu_size: size of tabu list
                reps: number of iterations searching neighbor solution
                max_iterations: maximum iterations of tabucol
                alpha: parameter of duration equation

            return

                solution: solution list applied tabucol
        """
        N = graph.order()
        colors = list(range(k))

        # Tabu List
        tabu = {}
        iterations = 0

        print(f"Initial Solution: {self.solution}")
        
        conflicts = 0
        aspiration_level = dict()
        while iterations < max_iterations:

            conflicts = self.count_conflicts(graph, self.solution)
            conflicting_nodes = set()
            for node in graph.nodes():
                for neighbor in graph.neighbors(node):
                    if self.solution[node] == self.solution[neighbor]:
                        conflicting_nodes.add(node)
                        conflicting_nodes.add(neighbor)

            conflicting_nodes = list(conflicting_nodes)
            # Exit Condition
            if conflicts == 0:
                print("proper coloring found!!")
                break


            # Exploring Neighbor solutions
            new_solution = None
            for r in range(reps):
                node = conflicting_nodes[randrange(0,len(conflicting_nodes))]

                # allocate best color: generating minimum conflicts
                new_color = self.choose_color(graph, self.solution, node, colors)
                new_solution = self.solution.copy()
                new_solution[node] = new_color

                new_conflicts = self.count_conflicts(graph, new_solution)

                L = randrange(0,9)
                # duration = L + f(s)*alpha
                duration = int(L + new_conflicts * alpha)

                # If found a better solution,
                if new_conflicts < conflicts:
                    # if f(s') <= A(f(s))
                    if new_conflicts <= aspiration_level.setdefault(conflicts, conflicts-1):
                        # set A(f(s)) = f(s')-1
                        aspiration_level[conflicts] = new_conflicts - 1

                        if (node, new_color) in tabu and tabu[(node, new_color)] > iterations:
                            tabu.pop((node, new_color))
                        else:
                            tabu[(node, new_color)] = iterations + duration

                    # case for found good solution but that action is in tabu, then should search more
                    else:
                        if (node, new_color) in tabu:
                            continue
                        else:
                            tabu[(node, new_color)] = iterations + duration

                    break


            self.solution = new_solution

            # Clean up expired tabu entries
            tabu = {move: expiry for move, expiry in tabu.items() if expiry > iterations}

            iterations += 1
            if iterations % 10 == 0:
                print(f"Iteration: {iterations}, Conflicts: {conflicts}")
                #self.writer.add_scalar("charts/conflicts", conflicts, iterations)
                #self.writer.add_scalar("charts/colors_used", len(np.unique(self.solution)), iterations) 
                if self.is_track:
                    wandb.log({"Iterations":iterations, "Conflicts":conflicts})
                if iterations % 100 == 0:
                    self.render(self.solution)

        print("final solution: ",self.solution)
        # After all iterations, return solution
        return self.solution



    def count_conflicts(self,graph, solution, node=None):
        """
        function count_conflicts() calculates number of conflicts given graph and solution.

            parameter

                graph: networkx graph

                solution:

                node: if node is given, only search conflicts around the node


            return

                conflicts: number of conflicts

        """

        conflicts = 0
        if node is None:
            for node in graph.nodes():
                for neighbor in graph.neighbors(node):
                    if solution[node] == solution[neighbor]:
                        conflicts += 1
            
            conflicts = conflicts // 2

        else:
            for neighbor in graph.neighbors(node):
                if solution[node] == solution[neighbor]:
                    conflicts += 1

        return conflicts




    def choose_color(self,graph, solution, node, colors):
        """
        function choose_color() chooses best color given target node.
        Best color means the color which makes minimal conflicts

            parameter

                graph: networkx graph

                solution:

                node: target node

                colors: color array


            return

                best_color

        """

        min_conflicts = float('inf')
        best_color = solution[node]
        for color in colors:
            if color != solution[node]:
                temp_solution = solution.copy()
                temp_solution[node] = color
                conflicts = self.count_conflicts(graph, temp_solution,node)
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_color = color

        return best_color




    def solve(self):
        """
        function solve literally do tabucol algorithm

        """

        self.tabucol(self.graph, self.k)
        
        self.close()



    def close(self):
        """
        function close() organizes and closes functions

        """
        
        if self.is_track:
            self.writer.close()
            wandb.finish()
