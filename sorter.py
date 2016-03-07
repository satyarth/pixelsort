import random


def sort_image(pixels, intervals, args):
    sorted_pixels = []
    for y in range(len(pixels)):
        row = []
        x_min = 0
        for x_max in intervals[y]:
            interval = []
            for x in range(x_min, x_max):
                interval.append(pixels[y][x])
            if random.randint(0, 100) >= args.randomness:
                row += sort_interval(interval, args.sorting_function)
            else:
                row += interval
            x_min = x_max
        row.append(pixels[y][0])
        sorted_pixels.append(row)
    return sorted_pixels


def sort_interval(interval, sorting_function):
    return [] if interval == [] else sorted(interval, key=sorting_function)
