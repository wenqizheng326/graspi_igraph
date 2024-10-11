import argparse
import igraph_testing
import testFileMaker
import csvFileMaker
import os

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("n", help="Number of nodes each side")
    parser.add_argument("dimension", choices=["2D", "3D"], help="Dimension of the graph")

    parser.add_argument("function", choices=["generate", "filter", "shortest_path"])

    args = parser.parse_args()
    filename = args.dimension + "-testFile/testFile-" + args.n + "-" + args.dimension + ".txt"
    if not os.path.exists(filename):
        testFileMaker.testFileMaker(int(args.n), int(args.dimension[:1]), filename)


    if args.function == "generate":
        print("Generating results")
        print("Memory usage of graph created by edges: " + str(csvFileMaker.functionMemory(igraph_testing.generateGraph, filename)) + " bytes")
        print("Memory usage of graph created by adjacency list: " + str(csvFileMaker.functionMemory(igraph_testing.generateGraphAdj, filename)) + " bytes")
        print("Completed")

    if args.function == "filter":
        g = igraph_testing.generateGraph(filename)
        g2 = igraph_testing.generateGraphAdj(filename)
        print("Generating results")
        print("Memory usage of graph filtering (edges): " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, g)) + " bytes")
        print("Memory usage of graph filtering (adjacency list): " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, g2)) + " bytes")
        print("Completed")

    if args.function == "shortest_path":
        g = igraph_testing.generateGraph(filename)
        g2 = igraph_testing.generateGraphAdj(filename)
        fg = igraph_testing.filterGraph(g)
        fg2 = igraph_testing.filterGraph(g2)
        print("Generating results")
        print("Memory usage of shortest path (edges): " + str(csvFileMaker.functionMemory(igraph_testing.shortest_path, fg)) + " bytes")
        print("Memory usage of shortest path (adjacency list): " + str(csvFileMaker.functionMemory(igraph_testing.shortest_path, fg2)) + " bytes")
        print("Completed")

if __name__ == "__main__":
    main()




