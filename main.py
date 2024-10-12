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
        print("Generating results\n")
        print("Memory usage of graph created by edges: " + str(csvFileMaker.functionMemory(igraph_testing.generateGraph, filename)) + " bytes")
        print("Runtime of graph created by edges: " + str(csvFileMaker.functionRuntime(5, igraph_testing.generateGraph, filename)) + " seconds\n")
        print("Memory usage of graph created by adjacency list: " + str(csvFileMaker.functionMemory(igraph_testing.generateGraphAdj, filename)) + " bytes")
        print("Runtime of graph created by adjacency list: " + str(csvFileMaker.functionRuntime(5, igraph_testing.generateGraphAdj, filename)) + " seconds\n")
        print("Memory usage of graph created by lattice: " + str(csvFileMaker.functionMemory(igraph_testing.lattice, filename)) + " bytes")
        print("Runtime of graph created by lattice: " + str(csvFileMaker.functionRuntime(5, igraph_testing.lattice, filename)) + " seconds\n")
        print("Completed")

    if args.function == "filter":
        g = igraph_testing.generateGraph(filename)
        g2 = igraph_testing.generateGraphAdj(filename)
        g3 = igraph_testing.lattice(filename)
        print("Generating results\n")
        print("Memory usage of graph filtering by edges: " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, g)) + " bytes")
        print("Runtime of graph filtering by edges: " + str(csvFileMaker.functionRuntime(5, igraph_testing.filterGraph, g)) + " seconds\n")
        print("Memory usage of graph filtering by adjacency list: " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, g2)) + " bytes")
        print("Runtime of graph filtering by adjacency list: " + str(csvFileMaker.functionRuntime(5, igraph_testing.filterGraph, g2)) + " seconds\n")
        print("Memory usage of graph filtering by lattice: " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, g3)) + " bytes")
        print("Runtime of graph filtering by lattice: " + str(csvFileMaker.functionRuntime(5, igraph_testing.filterGraph, g3)) + " seconds\n")
        print("Completed")

    if args.function == "shortest_path":
        g = igraph_testing.generateGraph(filename)
        g2 = igraph_testing.generateGraphAdj(filename)
        g3 = igraph_testing.lattice(filename)
        fg = igraph_testing.filterGraph(g)
        fg2 = igraph_testing.filterGraph(g2)
        fg3 = igraph_testing.filterGraph(g3)
        print("Generating results\n")
        print("Memory usage of shortest path by edges: " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, fg)) + " bytes")
        print("Runtime of shortest path by edges: " + str(csvFileMaker.functionRuntime(5, igraph_testing.filterGraph, fg)) + " seconds\n")
        print("Memory usage of shortest path by adjacency list: " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, fg2)) + " bytes")
        print("Runtime of shortest path by adjacency list: " + str(csvFileMaker.functionRuntime(5, igraph_testing.filterGraph, fg2)) + " seconds\n")
        print("Memory usage of shortest path by lattice: " + str(csvFileMaker.functionMemory(igraph_testing.filterGraph, fg3)) + " bytes")
        print("Runtime of shortest path by lattice: " + str(csvFileMaker.functionRuntime(5, igraph_testing.filterGraph, fg3)) + " seconds\n")
        print("Completed")

if __name__ == "__main__":
    main()




