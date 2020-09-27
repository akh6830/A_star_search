"""
Author: Min Kyi Htun
"""

from math import *
from queue import PriorityQueue

from PIL import Image

import Orienteering

map_i = Image.open("terrain.PNG").convert('RGB')
Orienteering.PIXELS, Orienteering.ELEVATION, Orienteering.GOAL_POINTS = \
    Orienteering.processMap(map_i, "elevation.txt", "brown.txt")


COLOR = (255, 0, 0)


def getNeightbors(x, y, x_edge, y_edge):
    """
    Get the neighboring coordinates of a particular pixel coordinate
    :param x: x coordinate of the pixel
    :param y: y coordinate of the pixel
    :param x_edge: column bound
    :param y_edge: row bound
    :return: return a list of neighboring pixels coordinates
    """
    return [(x2, y2) for x2 in range(x - 1, x + 2)
            for y2 in range(y - 1, y + 2)
            if (-1 < x <= x_edge and
                -1 < y <= y_edge and
                (x != x2 or y != y2) and
                (0 <= x2 <= x_edge) and
                (0 <= y2 <= y_edge))]


def search_path(start, final):
    # store g(n) as dictionary
    cost = {start: 0}

    # initialize priority queue
    pq = PriorityQueue()

    # keep track of predecessors to eventually get the path
    predecessors = {}

    # push the starting node onto the pq
    pq.put((0, start))

    # store f(n) as dictionary
    f_cost = {start: Orienteering.calculateCost(start, final)}

    path = []

    while not pq.empty():
        cur_pix = pq.get()[1]
        if cur_pix == final:
            while cur_pix != start:
                path.insert(0, cur_pix)
                cur_pix = predecessors[cur_pix]
            path.insert(0, start)
            break

        neighbors = getNeightbors(cur_pix[0], cur_pix[1], Orienteering.IMG_WIDTH, Orienteering.IMG_HEIGHT)

        for neighbor in neighbors:
            g = cost[cur_pix] + Orienteering.calculateCost(neighbor, cur_pix)
            h = Orienteering.calculateCost(final, neighbor)

            if neighbor not in cost or g + h < f_cost[neighbor]:
                f_cost[neighbor] = g + h
                cost[neighbor] = g
                pq.put((g+h, neighbor))
                predecessors[neighbor] = cur_pix

    return path
