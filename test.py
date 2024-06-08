from gcp_solver import GCP_Solver
import networkx as nx
import random
import argparse

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


def parse_arguments():
    parser = argparse.ArgumentParser(description="GCP-solver")
    parser.add_argument("--is_read_file", type=bool, required=True, help="whether using graph file")
    parser.add_argument("--graph_path", type=str, required=True, help="Path to the graph file")
    parser.add_argument("--graph_type", type=int, required=True, help="0 for random, 4 for flat, 5 for le450, 6 for queen, 7 for games120 and 8 for myciel")
    parser.add_argument("--nodes", type=int, required=True, help="Number of nodes")
    parser.add_argument("--k", type=int, required=True, help="Number of colors")
    parser.add_argument("--probability", type=float, required=True, help="probability for generating edges")
    parser.add_argument("--is_track", type=bool, required=True, help="whether tracking to WanDB")

    return parser.parse_args()


# main fuhction
if __name__ == "__main__":
    
    args = parse_arguments()

    gcp_solver = GCP_Solver(args.is_read_file,args.graph_path,args.graph_type,args.nodes,args.probability,args.k,args.is_track,"human","tabucol")
    gcp_solver.solve()
    



