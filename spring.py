"""
Author: Min Kyi Htun
"""

from PIL import ImageDraw
import Orienteering
import summer
from queue import PriorityQueue

MUD_COLOR = (144, 108, 63)


def springBFS(map_im, water_edges):
    mud = []

    explored = set()

    for pix in water_edges:
        queue = []
        queue.append(pix)

        while len(queue) != 0:
            curr_pix = queue.pop(0)

            if abs(curr_pix[0] - pix[0]) == 15 or abs(curr_pix[1] - pix[1]) == 15:
                break

            if curr_pix in explored:
                continue
            explored.add(curr_pix)
            neighbors = summer.getNeightbors(curr_pix[0], curr_pix[1], Orienteering.IMG_WIDTH, Orienteering.IMG_HEIGHT)
            for neighbor in neighbors:
                if neighbor in explored or neighbor in queue or \
                        (Orienteering.PIXELS[neighbor[0], neighbor[1]] == (0, 0, 255)) or \
                        (Orienteering.PIXELS[neighbor[0], neighbor[1]] == (205, 0, 101)) or \
                        ((float(Orienteering.ELEVATION[neighbor[1]][neighbor[0]]) -
                         float(Orienteering.ELEVATION[pix[1]][pix[0]])) > 1):
                    continue
                queue.append(neighbor)
                if Orienteering.PIXELS[neighbor[0], neighbor[1]] != (0, 0, 255):
                    mud.append(neighbor)

        while len(queue) != 0:
            curr_pix = queue.pop(0)
            if curr_pix in explored or curr_pix in queue or \
                    (Orienteering.PIXELS[curr_pix[0], curr_pix[1]] == (0, 0, 255)) or \
                    (Orienteering.PIXELS[curr_pix[0], curr_pix[1]] == (205, 0, 101)) or \
                    ((float(Orienteering.ELEVATION[curr_pix[1]][curr_pix[0]]) -
                      float(Orienteering.ELEVATION[pix[1]][pix[0]])) > 1):
                mud.append(curr_pix)

    draw_spring_terrain(map_im, mud)


def draw_spring_terrain(map_im, mud):
    drawing = ImageDraw.Draw(map_im)
    for i in range(len(mud)-1):
        drawing.point(mud[i], fill=MUD_COLOR)
    map_im.save('spring.png', "PNG")


def search_path(start, final):
    Orienteering.SPEED[(144, 108, 63)] = 3
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