"""
Author : Min Kyi Htun
"""
from math import *
from PIL import ImageDraw
from summer import *
import winter
import spring
import sys

SPEED = {(248, 148, 18): 8, (255, 192, 0): 3, (255, 255, 255): 7, (2, 208, 60): 5, (2, 136, 40): 2, (5, 73, 24): 1,
         (0, 0, 255): 4, (71, 51, 3): 10, (0, 0, 0): 9, (205, 0, 101): 0.1}

IMG_WIDTH = None
IMG_HEIGHT = None
PIXELS = None
ELEVATION = None
GOAL_POINTS = None


def processMap(map_im, elevation_f, goalp_f):
    """
    Process the map image (.png) with PILLOW(Python Image Library)
    :param map_im: image of the map
    :param elevation_f: information about elevation of each pixel in image in .txt file
    :param goalp_f: points we need to visit on our path representing x, y in .txt file
    :return: 2d list like object of pixels from the image and list of elevation and points to visit
    """
    # process the image
    global IMG_WIDTH
    global IMG_HEIGHT
    IMG_WIDTH, IMG_HEIGHT = map_im.size
    pixels = map_im.load()

    # process the elevation
    elevation_file = open(elevation_f)
    elevation = []
    for line in elevation_file:
        elevation.append(line.split())

    # process the goal points
    goalp_file = open(goalp_f)
    goal_points = []
    for line in goalp_file:
        goal_points.append(line.split())

    return pixels, elevation, goal_points


def calculateCost(next_pix, current_pix):
    """
    This function is used for A* search both to calculate real cost and heuristic cost
    for heuristic cost, use the final pixel to get to instead of neighboring pixel
    :param next_pix: goal pixel
    :param current_pix: starting pixel
    :return: return the cost of path (in this case time)
    """

    distance = None
    # movement in x direction
    if abs(next_pix[0] - current_pix[0]) == 1 and next_pix[1] == current_pix[1]:
        distance = 10.29
    # movement in y direction
    elif next_pix[0] == current_pix[0] and abs(next_pix[1] - current_pix[1]) == 1:
        distance = 7.55
    # diagonal movement
    else:
        distance = sqrt(((next_pix[0] - current_pix[0])*10.29)**2 +
                        ((next_pix[1]-current_pix[1])*7.55)**2)
    # consider the elevation in calculating distance
    distance = sqrt(distance**2 + (float(ELEVATION[next_pix[1]][next_pix[0]]) -
                                   float(ELEVATION[current_pix[1]][current_pix[0]]))**2)

    speed = SPEED[PIXELS[current_pix[0], current_pix[1]]]

    # modify the speed if we have different elevation between two pixels
    if float(ELEVATION[next_pix[1]][next_pix[0]]) == float(ELEVATION[current_pix[1]][current_pix[0]]):
        pass
    elif float(ELEVATION[next_pix[1]][next_pix[0]]) < float(ELEVATION[current_pix[1]][current_pix[0]]):
        elevation_dif = float(ELEVATION[current_pix[1]][current_pix[0]]) - float(ELEVATION[next_pix[1]][next_pix[0]])
        speed = speed * (1 + (elevation_dif/100))
    else:
        elevation_dif = float(ELEVATION[next_pix[1]][next_pix[0]]) - float(ELEVATION[current_pix[1]][current_pix[0]])
        speed = speed * (1 - (elevation_dif/100))
    time = distance/speed
    return time


def draw_on_im(im, full_path, color, output_f):
    drawing = ImageDraw.Draw(im)
    drawing.line(full_path, fill=color, width=1)
    im.save(output_f, "PNG")
    im.show()


def main():
    terrain = sys.argv[1]
    ele_f = sys.argv[2]
    path_f = sys.argv[3]
    season = sys.argv[4]
    output_f = sys.argv[5]
    map_im = Image.open(terrain).convert('RGB')
    global PIXELS
    global ELEVATION
    global GOAL_POINTS
    global SPEED
    PIXELS, ELEVATION, GOAL_POINTS = processMap(map_im, ele_f, path_f)
    full_path = []

    if season == "summer":

        for i in range(len(GOAL_POINTS)-1):
            start = GOAL_POINTS[i]
            end = GOAL_POINTS[i+1]
            start_tuple = (int(start[0]), int(start[1]))
            end_tuple = (int(end[0]), int(end[1]))
            full_path = full_path + search_path(start_tuple, end_tuple)
        draw_on_im(map_im, full_path, (255, 0, 0), output_f)

    elif season == "winter":

        water_edges = winter.get_water_edges()
        winter.waterBFS(map_im, water_edges)
        map_im = Image.open("winter.png")
        # global SPEED
        PIXELS, ELEVATION, GOAL_POINTS = processMap(map_im, "elevation.txt", "brown.txt")
        SPEED[(0, 0, 255)] = 0.1
        SPEED[(165, 242, 243)] = 5

        for i in range(len(GOAL_POINTS)-1):
            start = GOAL_POINTS[i]
            end = GOAL_POINTS[i+1]
            start_tuple = (int(start[0]), int(start[1]))
            end_tuple = (int(end[0]), int(end[1]))
            full_path = full_path + winter.search_path(start_tuple, end_tuple)
        draw_on_im(map_im, full_path, (255, 0, 0), output_f)

    elif season == "spring":
        water_edges = winter.get_water_edges()
        spring.springBFS(map_im, water_edges)
        map_im = Image.open("spring.png")
        # global SPEED
        PIXELS, ELEVATION, GOAL_POINTS = processMap(map_im, "elevation.txt", "brown.txt")
        SPEED[(144, 108, 63)] = 3

        for i in range(len(GOAL_POINTS)-1):
            start = GOAL_POINTS[i]
            end = GOAL_POINTS[i+1]
            start_tuple = (int(start[0]), int(start[1]))
            end_tuple = (int(end[0]), int(end[1]))
            full_path = full_path + spring.search_path(start_tuple, end_tuple)
        draw_on_im(map_im, full_path, (255, 0, 0), output_f)


if __name__ == '__main__':
    main()
