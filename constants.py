import interval
import sorting

black_pixel = (0, 0, 0, 255)
white_pixel = (255, 255, 255, 255)
defaults = {
    "interval_function": "threshold",
    "lower_threshold": 0.25,
    "upper_threshold": 0.8,
    "clength": 50,
    "angle": 0,
    "randomness": 0,
    "sorting_function": "lightness",
}
choices = {
    "interval_function": {
        "random": interval.random,
        "threshold": interval.threshold,
        "edges": interval.edge,
        "waves": interval.waves,
        "file": interval.file_mask,
        "file-edges": interval.file_edges,
        "none": interval.none
    },
    "sorting_function": {
        "lightness": sorting.lightness,
        "hue": sorting.hue,
        "intensity": sorting.intensity,
        "minimum": sorting.minimum,
        "saturation": sorting.saturation
    },
}