#ifndef GCP_SOLVER_H
#define GCP_SOLVER_H

#include <iostream>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <algorithm>
#include <numeric>
#include <random>
#include <ctime>
#include <cstdlib>
#include <fstream>
#include <sstream>

#define MAX_NUM	12345678


using namespace std;

struct pair_hash{
    template <class T1, class T2>
    size_t operator() (const pair<T1,T2>& pair) const{
	    return hash<T1>()(pair.first) ^ hash<T2>()(pair.second);
    }
};


class GCP_Solver{

 public:

   GCP_Solver(const vector<vector<int>>& target_graph, int k, string algorithm="tabucol");

   std::pair<vector<int>, int> solve();


 private:

   std::pair<vector<int>, int> tabucol(const vector<int>& solution, int k, int tabu_size=7, int reps=150, int max_iterations=3000, float alpha=0.6);

   int count_conflicts(const vector<int>& solution, int node=-1);

   int choose_color(const vector<int>& solution, int node, float p=0.7);

   void print_graph();
   
   void print_solution(const vector<int>& solution);

   int nodes;
   int k;

   vector<vector<int>> graph;

   string algorithm;

   vector<int> solution;

   unordered_map<pair<int,int>,int,pair_hash> tabu_list;
};

#endif



