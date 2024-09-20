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
    with open(fileName,'r') as file:
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
    secondToLastRow = num**2 - num
    offset = 0
    greenVertex = num**2+1


    for z in range(dimension):
        offset = z * (num**2)
        for y in range(num**2):
            if z < (dimension - 1):
                edge.append([y+offset,(y+offset+(num**2))])


        for x in range(0,secondToLastRow,num):
            x_num = x + num + offset
            x_offset = x+offset

            edge.append([x_offset,x_num])
            edge.append([x_offset,x_num+1])
            edge.append([x_offset,(x_offset+1)])

            for i in range(1,num):
                xi = x+i+offset
                edge.append([xi,(xi+num)])
                edge.append([(xi),(xi+(num-1))]) # right to left diagonals

                if i < num-1:
                    edge.append([xi,xi+1+num]) # left to right diagonals bottom row
                    edge.append([xi,xi+1]) # horizontal except first column
                    if x == secondToLastRow - num:
                        edge.append([secondToLastRow+i+offset,secondToLastRow+offset+i+1]) # horizontal last row except first column
            
    edge.append([(secondToLastRow+offset),(secondToLastRow+1+offset)]) # horizontal last row first column

    return edge

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
    depth = int(line[len(line)-2])

    g = ig.Graph(n = len(labels),edges=edges, directed=False, vertex_attrs={'color':labels})

    # Generate labels starting from 1
    # g.vs['label'] = [convert_to_1_based(i) for i in range(len(g.vs))]
   
    layout = g.layout('grid')  

    ''' ---- Running basic algorithms ----'''
       
    return g

def visual2D(g):
    layout = g.layout('grid')  
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
    edgeList = graph.get_edgelist()
    keptEdges = []

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if(graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges.append(edge)
    
    filteredGraph = graph.subgraph_edges(keptEdges,delete_vertices = False)

    return filteredGraph

'''********* Shortest Path **********'''
def shortest_path(graph,file):
    numVertices = graph.vcount()
    greenVertex = numVertices
    graph.add_vertices(1)
    edgesToAdd = []
    listOfShortestPaths = {}
    numBottomLayers = 0
    numBottomRowVertices = 0

    with open(file,'r') as f:
        line = f.readline()
        line = line.split()
        numBottomLayers = int(line[2])
        numBottomRowVertices = int(line[0])

    for x in range(numBottomLayers):
        offset = x * numBottomLayers
        for i in range(numBottomRowVertices):
                edgesToAdd.append([greenVertex,i+offset])

    graph.add_edges(edgesToAdd)

    for x in range(numVertices):
        if graph.vs[x]['color'] == 'black':
            listOfShortestPaths[x] = graph.get_shortest_paths(greenVertex,x,output="vpath")
    
    return listOfShortestPaths
    


    

