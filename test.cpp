#include "gcp_solver.h"

// Function to read a DIMACS graph file and construct an adjacency matrix
vector<vector<int>> readDIMACS_graph(const string& graph_file_path) {
    vector<vector<int>> graph;
    ifstream infile(graph_file_path);
    string line;

    if (!infile.is_open()) {
        cerr << "Error opening file: " << graph_file_path << endl;
        exit(EXIT_FAILURE);
    }

    while (getline(infile, line)) {
        if (line.empty() || line[0] == 'c') {
            continue; // Skip comment lines
        }

        istringstream iss(line);
        string type;
        iss >> type;

        if (type == "p") {
            // Problem line: p <format> <nodes> <edges>
            string format;
            int nodes, edges;
            iss >> format >> nodes >> edges;
            graph.resize(nodes, vector<int>(nodes, 0)); // Initialize the adjacency matrix
        } else if (type == "e") {
            // Edge line: e <node1> <node2>
            int u, v;
            iss >> u >> v;
            graph[u-1][v-1] = 1; // Decrement by 1 to handle 0-based indexing
            graph[v-1][u-1] = 1; // Ensure the graph is undirected
        }
    }

    infile.close();
    return graph;
}


int main(int argc, char* argv[]){
 
 if(argc != 3){
    cerr << "Usage: " << argv[0] << " <graph_file_path> <num_colors> <algorithm>" << endl;
    return EXIT_FAILURE;
 }

 string graph_file_path = argv[1];
 int num_colors = stoi(argv[2]);

 vector<vector<int>> test_graph = readDIMACS_graph(graph_file_path);

 GCP_Solver gcp_solver = GCP_Solver(test_graph,num_colors,"pg_tabucol");
 gcp_solver.solve();

 return 0;
}
