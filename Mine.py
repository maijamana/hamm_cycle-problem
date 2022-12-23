"""
Project number 6.
"""
import csv

def read_csv(file_name, weight = False):
    """
    Function read csv file with 3 colums of numbers and returns 2 dictionaries:
    first: {verticl from which we start moving: [verticl to which we moving]}
    second: {first verticl of the pair: weight of the edge of the graph}
    Args:
        file_name: the path to file with graph
        weight: True if graph is !!!!!!!!!!!!!!!!!!!!!!!!!!11
    Returns:
        dict[int:list] - graph by dictionary
        List[list] - the adjacency matrix
    """
    try:
        with open(
            file_name,
            mode="r",
            encoding="utf-8",
        ) as infile:
            reader = csv.reader(infile)
            mydict = {}
            for rows in reader:
                try:
                    mydict[int(rows[0])] += [int(rows[1])]
                except KeyError:
                    mydict[int(rows[0])] = [int(rows[1])]
                try:
                    mydict[int(rows[1])] += [int(rows[0])]
                except KeyError:
                    mydict[int(rows[1])] = [int(rows[0])]
        if weight:
            res = {}
            with open(file_name, 'r',encoding="utf-8") as infile:
                lines = infile.readlines()
                for line in lines:
                    triple = line.split(',')
                    res[(int(triple[0]), int(triple[1]))] = int(triple[2])
            
            return tuple([mydict,res])
        return tuple([mydict])
    except NotADirectoryError:
        print("Not a correct path.")

def dfs(graph):
    """
    perform dfs on the graph and store its result
    in the list of vertices(integers that represent vertices)
    :rtype: list(int)
    :param graph:  dict(key=int, value=list(int))
    :return: dfs-result
    """
    key = list(graph.keys())[0]
    stack = [key]
    order = [key]
    while stack:
        key = stack[-1]
        if any(value not in order for value in graph[key]):
            min_val = [val for val in graph[key] if val not in order]
            stack.append(min(min_val))
            order.append(min(min_val))
        else:
            stack.pop()
    return order

def hamm_cycle(file_name, weight = False):
    '''
    This function solves Hamiltonian path problem
    Args:
        file_name: the path to file with graph
        weight: uses only to !!!!!!!!!!!!!!!!!!!!! graphs
    Returns:
        List[int] - hamiltonian cycle in graph
    '''
    graph = read_csv(file_name, weight = weight)
    if not weight:
        vertex = dfs(graph[0])
    else:
        procent = (len(graph[0].keys())//20)+1
        maximum = dict(sorted(graph[1].items(), key=lambda item: item[1]))
        vertex = dfs(graph[0])
        keys = list(maximum.keys())
        for i in range(procent):
            index1 = vertex.index(keys[-i-1][0])
            index2 = vertex.index(keys[-i-1][1])
            if abs(index1-index2)==1:
                if index1!=0:
                    vertex[index1-1],vertex[index1] = vertex[index1],vertex[index1-1]
                else:
                    vertex[index2+1],vertex[index2] = vertex[index2],vertex[index2+1]
    print(vertex)
    print(graph[0])
    trueth = 0
    i = 0
    len_graph = len(graph[0])+1
    while trueth != len_graph:
        trueth += 1
        if vertex[i+1] in graph[0][vertex[i]]:
            vertex.append(vertex[i])
            vertex.remove(vertex[i])
        else:
            for j in range(i+2, len(vertex)-1):
                try:
                    if (vertex[i] in graph[0][vertex[j]]) and (vertex[i+1] in graph[0][vertex[j+1]]):
                        vertex_p = vertex[:(i+1)] + list(reversed(vertex[(i+1):(j+1)])) + vertex[(j+1):]
                        vertex = vertex_p
                        vertex.append(vertex[i])
                        vertex.remove(vertex[i])
                        break
                except IndexError:
                    return 'Граф не підпадає під теореми Дірака та Оре'
    ind = vertex.index(1)
    return vertex[ind:]+vertex[:ind]+[1]
