import queue
from math import sqrt

from utils import DIRECTION_DICT

"""
From last assignment. Btw bfs doesn't return the right distances..
"""


def euclidean_distance(coord1, coord2):
    """
    WE USE IT AS THE COST FUNCTION FOR G AND H

    In mathematics, the Euclidean distance between two points is the length of
    a line segment between the two points.

    Basically you use the Pythagorean theorem: a^2 + b^2 = c^2 where:
    * a = (coord2.x - coord1.x)
    * b = (coord2.y - coord1.y)
    * c = the distance between coord1 and coord2

    :return: Euclidean distance
    """
    return sqrt((coord2[0] - coord1[0]) * (coord2[0] - coord1[0]) + (coord2[1] - coord1[1]) * (coord2[1] - coord1[1]))


def getNeighbours(node, posValidFunc):
    """Get neighbours of node that are valid"""
    neighbours = [(node[0] + dist_coord[0], node[1] + dist_coord[1]) for dist_coord in DIRECTION_DICT.values()]  # get all 4 neighbours
    neighbours = [node for node in neighbours if posValidFunc(node[0], node[1])]  # check if neighbours are valid
    return neighbours


def evaluation_function_a_star(end, n, cost_dict):
    """
    f(n) = g(n) + h(n) where:
    * f(n) is the evaluation function
    * g(n) is the cost function from the initial state to the current state n
    * h(n) is the cost heuristic function from the current state to the final state

    :param end: end coordinates
    :param n: current coordinates
    :param cost_dict: for g function, the cost until now
    :return: f(n)
    """
    g = cost_dict[n]
    h = euclidean_distance(n, end)  # heuristic function = smart guess
    return g + h


def bestFirstSearch(start, destination, f, posValidFunc):
    """
    Get the shortest path
    :param start: start coordinates
    :param destination: coordinates
    :param f: function for priority queue
    :return: boolean(if it was found or not) + the predecessors' dictionary.
    """
    found = False
    predecessor = {start: -1}  # save predecessors to recreate the path if it exists
    cost_dict = {start: 0}  # for g function

    visited = []
    toVisit = queue.PriorityQueue()  # FIFO sorted list (priority queue)
    toVisit.put((f(start, cost_dict), start))

    while not toVisit.empty() and not found:
        if toVisit.empty():  # ask this: why is it here if we have the while ????
            return False, []
        node = toVisit.get(block=False)[1]  # do not block until an item is available

        if node not in visited:
            visited.append(node)
        else:
            continue

        if node == destination:
            found = True
        else:
            neighbours = getNeighbours(node, posValidFunc)
            for neighbour in neighbours:
                if neighbour not in visited:
                    cost_dict[neighbour] = cost_dict[node] + 1  # update cost
                    toVisit.put((f(neighbour, cost_dict), neighbour))
                    predecessor[neighbour] = node

    return found, predecessor


def computePath(predecessors, end):
    """From the dict of predecessors, compute the shortest path from start to destination"""
    path = []
    while end != -1:
        path.append(end)
        end = predecessors[end]
    path.reverse()
    return path


def AStarAlgorithm(start, destination, posValidFunc):
    path = bestFirstSearch(
        start, destination,
        lambda current, cost_dict: evaluation_function_a_star(destination, current, cost_dict),  # f function
        posValidFunc
    )

    if not path[0]:
        return []
    else:
        return computePath(path[1], destination)