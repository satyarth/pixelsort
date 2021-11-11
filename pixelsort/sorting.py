import functools
import typing


@functools.cache
def lightness(pixel: typing.Tuple[int, int, int]) -> float:
    """Sort by the lightness of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    return (minc + maxc) / 2.0


@functools.cache
def hue(pixel: typing.Tuple[int, int, int]) -> float:
    """Sort by the hue of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    # XXX Can optimize (maxc+minc) and (maxc-minc)
    if minc == maxc:
        return 0.0
    mcminusmc = maxc - minc
    rc = (maxc - r) / mcminusmc
    gc = (maxc - g) / mcminusmc
    bc = (maxc - b) / mcminusmc
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h


@functools.cache
def saturation(pixel: typing.Tuple[int, int, int]) -> float:
    """Sort by the saturation of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    l = (minc + maxc) / 2.0
    if minc == maxc:
        return 0.0
    if l <= 0.5:
        s = (maxc - minc) / (maxc + minc)
    else:
        s = (maxc - minc) / (2.0 - maxc - minc)
    return s


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
