from PIL import Image

SPEED = {(248, 148, 18): 8, (255, 192, 0): 3, (255, 255, 255): 7, (2, 208, 60): 5, (2, 136, 40): 2, (5, 73, 24): 1,
         (0, 0, 255): 4, (71, 51, 3): 10, (0, 0, 0): 9, (205, 0, 101): 0}


def processMap(map, elevation_f):
    """
    Process the map image (.png) with PILLOW(Python Image Library)
    :param map: image of the map (.png)
    :return: 2d list of pixels in the format list[y][x] from the image
    """
    map_im = Image.open(map).convert('RGB')
    width, height = map_im.size
    pixels = list(map_im.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    elevation_file = open(elevation_f)
    elevation = []
    for line in elevation_file:
        elevation.append(line.split())
    return pixels, elevation