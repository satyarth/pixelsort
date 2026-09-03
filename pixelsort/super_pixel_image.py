import numpy as np
from PIL import Image


class SuperPixelImage:
    def __init__(self, image: Image.Image, super_pixel_size: int):
        self.super_pixel_size = super_pixel_size
        self.source_image = image
        self.original_size = image.size
        self.scaled_image = (
            image.reduce(super_pixel_size) if super_pixel_size > 1 else image
        )
        self.size = self.scaled_image.size
        self.average_colors = np.asarray(self.scaled_image)
