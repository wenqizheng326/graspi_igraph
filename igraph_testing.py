import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

'''---------Function to create edges for graph in specified format --------'''


def edge(fileName):
    line = []
    n = ""
    d = ""
    dimension = 0
    with open(fileName, 'r') as file:
        line = file.readline()
        splitLine = line.split()
        numBottomLayers = int(splitLine[2])
        numBottomRowVertices = int(splitLine[0])
        for i in line:
            if i != ' ':
                n += i
            elif i == ' ':
                break
        for i in reversed(line):
            if i != ' ' and i != '\n':
                d += i
            elif i == ' ':
                break

        dimension = int(d[::-1])

    num = int(n)
    edge = []
    secondToLastRow = num ** 2 - num
    offset = 0
    blueVertex = num ** 2
    redVertex = num ** 2 + 1
    topOffset = (num ** 2) - num

    for x in range(numBottomLayers):
        offset = x * numBottomLayers
        for i in range(numBottomRowVertices):
            edge.append([blueVertex, i + offset])

    for x in range(numBottomLayers):
        offset = x * numBottomLayers

        for i in range(numBottomRowVertices):
            edge.append([redVertex, i + offset + topOffset])

    for z in range(dimension):
        offset = z * (num ** 2)
        for y in range(num ** 2):
            if z < (dimension - 1):
                edge.append([y + offset, (y + offset + (num ** 2))])

        for x in range(0, secondToLastRow, num):
            x_num = x + num + offset
            x_offset = x + offset

            edge.append([x_offset, x_num])
            edge.append([x_offset, x_num + 1])
            edge.append([x_offset, (x_offset + 1)])

            for i in range(1, num):
                xi = x + i + offset
                edge.append([xi, (xi + num)])
                edge.append([(xi), (xi + (num - 1))])  # right to left diagonals

                if i < num - 1:
                    edge.append([xi, xi + 1 + num])  # left to right diagonals bottom row
                    edge.append([xi, xi + 1])  # horizontal except first column
                    if x == secondToLastRow - num:
                        edge.append([secondToLastRow + i + offset,
                                     secondToLastRow + offset + i + 1])  # horizontal last row except first column

    edge.append([(secondToLastRow + offset), (secondToLastRow + 1 + offset)])  # horizontal last row first column

    return edge


def adjList(filename):
    adjacency_list = {}
    dimX = dimY = dimZ = 0

    with open(filename, "r") as file:
        header = file.readline().split(' ')
        dimX, dimY, dimZ = int(header[0]), int(header[1]), int(header[2])

        current_node = 0
        for z in range(dimZ):
            for y in range(dimY):
                for x in range(dimX):
                    neighbors = []

                    # Node to the left
                    if x > 0:
                        neighbors.append(current_node - 1)
                    # Node to the bottom
                    if y > 0:
                        neighbors.append(current_node - dimX)
                    # Node to Southwest
                    if y > 0 and x > 0:
                        neighbors.append(current_node - dimX - 1)
                    # Node to Southeast
                    if y > 0 and x < dimX - 1:
                        neighbors.append(current_node - dimX + 1)
                    # Node to previous dimension
                    if z > 0:
                        neighbors.append(current_node - dimX * dimY)

                    adjacency_list[current_node] = neighbors
                    current_node += 1

    # Add blue and red nodes outside the loop
    adjacency_list[dimZ * dimY * dimX] = list(range(dimX))
    adjacency_list[dimZ * dimY * dimX + 1] = [i + dimX * (dimY - 1) for i in range(dimX)]

    return adjacency_list


'''------- Labeling the color of the vertices -------'''
def vertexColors(fileName):
    labels = []
    with open(fileName, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            for char in line:
                if char == '1':
                    labels.append('white')
                elif char == '0':
                    labels.append('black')

    return labels

'''********* Constructing the Graph **********'''
def generateGraph(file):
    edges = edge(file)
    labels = vertexColors(file)

    f = open(file,'r')
    line = f.readline()
    line = line.split()
    
    g = ig.Graph(n = int(line[0])*int(line[1]),edges=edges, directed=False, vertex_attrs={'color':labels})
    g.vs[int(line[0]) * int(line[1])]['color'] = 'blue'
    g.vs[int(line[0]) * int(line[1]) + 1]['color'] = 'red'
       
    return g


def generateGraphAdj(file):
    edges = adjList(file)
    labels = vertexColors(file)

    f = open(file, 'r')
    line = f.readline()
    line = line.split()

    g = ig.Graph.ListDict(edges=edges, directed=False)
    g.vs["color"] = labels
    g.vs[int(line[0]) * int(line[1])]['color'] = 'blue'
    g.vs[int(line[0]) * int(line[1]) + 1]['color'] = 'red'

    return g

def visual2D(g):
    layout = g.layout('kk')
    fig, ax = plt.subplots()
    # ax.invert_yaxis() # reverse starting point of graph (vertex 0)

    ig.plot(g, target=ax, layout=layout,vertex_size=25,margin=5)

    ''' ---- generate the labels of each vertex value ---- '''
    for i, (x, y) in enumerate(layout):
        g.vs['label']=[i for i in range(len(g.vs))]
        ax.text(
            x, y - 0.2,
            g.vs['label'][i],
            fontsize=12,
            color='black',
            ha='right',  # Horizontal alignment
            va='top'  # Vertical alignment
        )

    plt.show()

def visual3D(g):
    edges = g.get_edgelist()
    num_vertices = len(g.vs)
    grid_size = int(np.round(num_vertices ** (1/3)))  

    # Generate 3D coordinates (layout) for the vertices
    x, y, z = np.meshgrid(range(grid_size), range(grid_size), range(grid_size))
    coords = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

    # Plot the graph in 3D using matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot vertices
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=g.vs['color'], s=100)

    # Plot edges
    for e in edges:
        start, end = e
        ax.plot([coords[start][0], coords[end][0]], 
                [coords[start][1], coords[end][1]], 
                [coords[start][2], coords[end][2]], 'black')

    # Add labels to the vertices
    for i, (x, y, z) in enumerate(coords):
        ax.text(x, y, z, str(i), color='black')

    plt.show() 



'''********* Filtering the Graph **********'''


def filterGraph(graph):
    keptEdges = [edge for edge in graph.get_edgelist()
                 if graph.vs[edge[0]]['color'] == graph.vs[edge[1]]['color']
                 or 'green' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}]

    return graph.subgraph_edges(keptEdges, delete_vertices=False)

'''********* Shortest Path **********'''


def shortest_path(graph):
    numVertices = graph.vcount()
    ccp = graph.connected_components()
    listOfShortestPaths = {}
    greenVertex = numVertices - 1

    for c in ccp:
        if graph.vs[c]['color'] == 'black':
            for x in c:
                if graph.vs[x]['color'] == 'black' or graph.vs[x]['color'] == 'green':
                    listOfShortestPaths[x] = graph.get_shortest_paths(greenVertex, x, output="vpath")[0]

    return listOfShortestPaths
    