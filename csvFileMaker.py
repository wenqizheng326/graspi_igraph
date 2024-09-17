import igraph_testing as ig
import time 
import psutil
import os
import csv

def functionRuntime(count,function, *argv):
    totaltime = 0
    
    for x in range(count):
        startTime = time.time()
        function(*argv)
        endTime = time.time()
        timeTaken = endTime - startTime
        totaltime += timeTaken

    avgExecution = totaltime / count

    return avgExecution

def functionMemory(function, *argv):

    process = psutil.Process(os.getpid())
    memBefore = process.memory_info().rss / 1024.0
    function(*argv)
    memAfter = process.memory_info().rss / 1024.0 
    memUsage = memAfter - memBefore
    
    return memUsage

def csvMaker(fileName, n, dim, count, graphGen, graphGenPar,graphFilt, graphFiltPar,shortPath, shortPathPar):
    row = [n,(n**dim)]
    totalTime = 0
    totalMem = 0

    graphGenRuntime = functionRuntime(count,graphGen,*graphGenPar)
    graphFiltRuntime = functionRuntime(count,graphFilt,*graphFiltPar)
    shortPathRuntime = functionRuntime(count,shortPath,*shortPathPar)

    totalTime = graphGenRuntime + graphFiltRuntime + shortPathRuntime
    totalTime = round(totalTime,20)
    
    graphGenMem = functionMemory(graphGen,*graphGenPar)
    graphFiltMem = functionMemory(graphFilt,*graphFiltPar)
    shortPathMem = functionMemory(shortPath,*shortPathPar)

    totalMem = graphGenMem + graphFiltMem + shortPathRuntime
    totalMem = round(totalMem,20)

    row.append(graphGenRuntime)
    row.append(graphFiltRuntime)
    row.append(shortPathRuntime)
    row.append(totalTime)
    row.append(totalMem)

    with open(fileName, 'a', newline = "\n") as file:
        writer = csv.writer(file)
        writer.writerow(row)


fileName = "2D-testFile/testFile-500-2D.txt"   
g = ig.generateGraph(fileName)

csvMaker("output.csv", 500, 2, 3, ig.generateGraph, [fileName], ig.filterGraph, [g], ig.shortest_path, [g,fileName])