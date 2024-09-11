import igraph as ig
import matplotlib.pyplot as plt


# Function to convert 0-based index to 1-based
# def convert_to_1_based(index):
#     return index 


'''---------Function to create edges for graph in specified format --------'''
def edge(fileName):
    line = []
    n = ""
    dimension = 0
    with open(fileName,'r') as file:
        line = file.readline()
        for i in line:
            if i != ' ':
                n += i
            elif i == ' ':
                break
        dimension = int(line[len(line)-2])
    num = int(n)
    edge = []
    secondToLastRow = num**2 - num
    for x in range(0,secondToLastRow,num):
        x_num = x + num

        edge.append([x,x_num])
        edge.append([x,x_num+1])
        edge.append([x,(x+1)])

        for i in range(1,num):
            xi = x+i
            edge.append([xi,(xi+num)])
            edge.append([(xi),(xi+(num-1))]) # right to left diagonals

            if i < num-1:
                edge.append([xi,xi+1+num]) # left to right diagonals bottom row
                edge.append([xi,xi+1]) # horizontal except first column
                if x == secondToLastRow - num:
                    edge.append([secondToLastRow+i,secondToLastRow+i+1]) # horizontal last row except first column
      
    edge.append([secondToLastRow,secondToLastRow+1]) # horizontal last row first column

    return edge

'''------- Labeling the color of the vertices -------'''
def vertexColors(fileName):
    labels = []
    with open(fileName, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            for char in line:
                if char == '0':
                    labels.append('white')
                elif char == '1':
                    labels.append('black')

    return labels


'''********* Constructing the Graph **********'''
def generateGraph(file):
    edges = edge(file)
    labels = vertexColors(file) 

    g = ig.Graph(n = len(labels),edges=edges, directed=False, vertex_attrs={'color':labels})

    # Generate labels starting from 1
    # g.vs['label'] = [convert_to_1_based(i) for i in range(len(g.vs))]
   
    layout = g.layout('grid')  

    ''' ---- Running basic algorithms ----'''
    # print(g.get_shortest_paths(0,24))

    ''' ---- Plot the graph in matplotlib for visuals ----'''
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

    plt.show() #displays matplot graph

    return g


# generateGraph("testFile-10.txt")      # 3.6 secs with visuals, 417 ms without
# generateGraph("testFile-50.txt")      # 13.258 secs with visuals, 427 ms without
# generateGraph("testFile-100.txt")     # 46.705 secs with visuals, 438 ms without
# generateGraph("testFile-500.txt")     # 967ms without 
# generateGraph("testFile-1000.txt")      # 2.522 secs without
# generateGraph("out.txt")
g = generateGraph("testFile-10-2D.txt")
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
    layout = filteredGraph.layout("grid")


    ''' Plot the graph in matplotlib for visuals '''
    fig, ax = plt.subplots()
    # ax.invert_yaxis() # reverse starting point of graph (vertex 0)

    ig.plot(filteredGraph, target=ax, layout=layout,vertex_size=25,margin=5,vertex_label = None)

    filteredGraph.vs['label']=[i for i in range(len(filteredGraph.vs))]
    ''' generate the labels of each vertex value '''
    for i, (x, y) in enumerate(layout):
        
        ax.text(
            x, y - 0.2,  
            filteredGraph.vs['label'][i],
            fontsize=12,
            color='black',  
            ha='right',  # Horizontal alignment
            va='top'  # Vertical alignment
        )

    plt.show() #displays matplot graph

    numCC = filteredGraph.connected_components()
    # print(numCC)

 
filterGraph(g)
