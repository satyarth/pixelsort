import pixelsort.util as util


def lightness(pixel):
    """Sort by the lightness of a pixel according to a HSV representation."""
    return util.lightness(pixel)


def intensity(pixel):
    """Sort by the intensity of a pixel, i.e. the sum of all the RGB values."""
    return pixel[0] + pixel[1] + pixel[2]


def hue(pixel):
    """Sort by the hue of a pixel according to a HSV representation."""
    return util.hue(pixel)


def saturation(pixel):
    """Sort by the saturation of a pixel according to a HSV representation."""
    return util.saturation(pixel)


def minimum(pixel):
    """Sort on the minimum RGB value of a pixel (either the R, G or B)."""
    return min(pixel[0], pixel[1], pixel[2])


choices = {
    "lightness": lightness,
    "hue": hue,
    "intensity": intensity,
    "minimum": minimum,
    "saturation": saturation
}
