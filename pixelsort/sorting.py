import typing
from colorsys import rgb_to_hsv


def lightness(pixel: typing.Tuple[int, int, int]) -> float:
    """Sort by the lightness of a pixel according to a HSV representation."""
    # For backwards compatibility with python2
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[2] / 255.0


def hue(pixel: typing.Tuple[int, int, int]) -> float:
    """Sort by the hue of a pixel according to a HSV representation."""
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[0] / 255.0


def saturation(pixel: typing.Tuple[int, int, int]) -> float:
    """Sort by the saturation of a pixel according to a HSV representation."""
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[1] / 255.0


def intensity(pixel: typing.Tuple[int, int, int]) -> int:
    """Sort by the intensity of a pixel, i.e. the sum of all the RGB values."""
    return pixel[0] + pixel[1] + pixel[2]


def minimum(pixel: typing.Tuple[int, int, int]) -> int:
    """Sort on the minimum RGB value of a pixel (either the R, G or B)."""
    return min(pixel[0], pixel[1], pixel[2])


choices = {
    "lightness": lightness,
    "hue": hue,
    "intensity": intensity,
    "minimum": minimum,
    "saturation": saturation
}
