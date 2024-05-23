from gcp_solver import GCP_Solver
import networkx as nx
import random


def load_testcase(file):
    graph = nx.Graph()
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            words = line.split()
            if words[0] == 'p':
                assert words[1] == 'edge'
                vertices = int(words[2])
                graph.add_nodes_from(range(vertices))
            if words[0] == 'e':
                graph.add_edge(int(words[1]) - 1, int(words[2]) - 1)
    return graph


# read graph data file and initialize graph
# file format: col, mtx,
def read_graph_from_file(path):
    graph = nx.Graph()

    if path[-3:].__contains__("col"):
        with open(path,"r") as f:
            for line in f.readlines():
                try:
                    #decoded_line = line.decode('utf-8')
                    if line[0] == "c":
                        continue
                    elif line[0] == "p":
                        n, m = line.split()[2:4]
                        n, m = int(n), int(m)
                        continue
                    elif line[0] == "e":
                        u, v = line.split()[1:3]
                        u, v = int(u), int(v)
                        graph.add_edge(u-1, v-1)
                        continue

                except UnicodeDecodeError as e:
                    print("error occured")
                    continue

    elif path[-3:].__contains__("mtx"):
        with open(path, "r") as f:
            for line in f.readlines():
                try:
                    #decoded_line = line.decode('utf-8')
                    if line[0] == "%":
                        continue
                    # if N,N,M appeared
                    elif len(line.split(' ')) == 3:
                        line = line.split(' ')
                        n = int(line[0])
                        m = int(line[2])
                        continue
                    else:
                        line = line.split(' ')
                        u = int(line[0])
                        v = int(line[1])
                        graph.add_edge(u-1, v-1)
                        continue

                except UnicodeDecodeError as e:
                    print("error occured")
                    continue


    return graph




# main fuhction
if __name__ == "__main__":
    
    graph = nx.gnp_random_graph(100,0.5)
    k = 60

    gcp_solver = GCP_Solver(graph,k,"human")
    gcp_solver.solve()
    



