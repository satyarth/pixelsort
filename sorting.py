import util


def lightness(pixel):
    return util.lightness(pixel)


def intensity(pixel):
    return pixel[0] + pixel[1] + pixel[2]


def maximum(pixel):
    return max(pixel[0], pixel[1], pixel[2])


def minimum(pixel):
    return min(pixel[0], pixel[1], pixel[2])
