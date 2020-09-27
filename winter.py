"""
Author: Min Kyi Htun
"""

from math import *
from queue import PriorityQueue
from PIL import Image, ImageDraw
import Orienteering
import summer


ICE_COLOR = (165, 242, 243)


def get_water_edges():
    water = []
    water_edges = []

    for x in range(Orienteering.IMG_WIDTH):
        for y in range(Orienteering.IMG_HEIGHT):
            if Orienteering.PIXELS[x, y] == (0, 0, 255):
                water.append((x, y))

    for pix in water:
        neighbors = summer.getNeightbors(pix[0], pix[1], Orienteering.IMG_WIDTH,
                                         Orienteering.IMG_HEIGHT)
        for pix1 in neighbors:
            if Orienteering.PIXELS[pix1[0], pix1[1]] != (0, 0, 255) and (pix not in water_edges):
                water_edges.append(pix)

    return water_edges


def draw_winter_terrain(map_im, safe_pix):
    drawing = ImageDraw.Draw(map_im)
    for i in range(len(safe_pix )-1):
        drawing.point(safe_pix[i], fill=ICE_COLOR)
    map_im.save('winter.png', "PNG")


def waterBFS(map_im, water_edges):
    safe_pixels = []

    explored = set()
    for pix in water_edges:

        queue = []
        queue.append(pix)

        while len(queue) != 0:
            curr_pix = queue.pop(0)

            if abs(curr_pix[0] - pix[0]) == 7 or abs(curr_pix[1] - pix[1]) == 7:
                break

            if curr_pix in explored:
                continue
            explored.add(curr_pix)
            neighbors = summer.getNeightbors(curr_pix[0], curr_pix[1], Orienteering.IMG_WIDTH, Orienteering.IMG_HEIGHT)
            for neighbor in neighbors:
                if neighbor in explored or neighbor in queue or \
                        (Orienteering.PIXELS[neighbor[0], neighbor[1]] != (0, 0, 255)):
                    continue
                queue.append(neighbor)
                if Orienteering.PIXELS[neighbor[0], neighbor[1]] == (0, 0, 255):
                    safe_pixels.append(neighbor)

        while len(queue) != 0:
            curr_pix = queue.pop(0)
            # print(len(queue))
            if Orienteering.PIXELS[curr_pix[0], curr_pix[1]] == (0, 0, 255):
                safe_pixels.append(curr_pix)

    draw_winter_terrain(map_im, safe_pixels)


def search_path(start, final):
    Orienteering.SPEED[(0, 0, 255)] = 0.1
    Orienteering.SPEED[(165, 242, 243)] = 5
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

        neighbors = summer.getNeightbors(cur_pix[0], cur_pix[1], Orienteering.IMG_WIDTH, Orienteering.IMG_HEIGHT)

        for neighbor in neighbors:
            g = cost[cur_pix] + Orienteering.calculateCost(neighbor, cur_pix)
            h = Orienteering.calculateCost(final, neighbor)

            if neighbor not in cost or g + h < f_cost[neighbor]:
                f_cost[neighbor] = g + h
                cost[neighbor] = g
                pq.put((g+h, neighbor))
                predecessors[neighbor] = cur_pix

    return path