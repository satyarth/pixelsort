from PIL import Image
from sorter import sort_image
from argparams import parse_args
import util
import logging
from constants import defaults, choices

def pixelsort(
        image,
        mask_image = None,
        interval_image = None,
        randomness: float = defaults["randomness"],
        clength: int = defaults["clength"],
        sorting_function: str = defaults["sorting_function"],
        interval_function: str = defaults["interval_function"],
        lower_threshold: float = defaults["lower_threshold"],
        upper_threshold: float = defaults["upper_threshold"],
        angle: int = defaults["angle"]
    ) -> Image.Image:


    logging.debug("Cleaning input image...")
    image.convert('RGBA').rotate(angle, expand=True)

    logging.debug("Getting data...")
    input_data = image.load()

    mask_data = None
    if mask_image:
        logging.debug("Loading mask...")
        mask_data = mask_image.convert('RGBA').rotate(angle, expand=True).resize(image.size, Image.ANTIALIAS).load()

    if interval_image:
        logging.debug("Loading interval image...")
        interval_image.convert('RGBA').rotate(angle, expand=True).resize(image.size, Image.ANTIALIAS)

    logging.debug("Getting pixels...")
    pixels = util.get_pixels(input_data, mask_data, image.size)

    logging.debug("Determining intervals...")
    try:
        interval_function = choices["interval_function"][interval_function]
    except KeyError:
        logging.warning("Invalid interval function specified, defaulting to 'threshold'.")
        interval_function = choices["interval_function"]["threshold"]
    intervals = interval_function(
        pixels,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        clength=clength,
        interval_image=interval_image,
        image=image
    )

    logging.debug("Sorting pixels...")
    try:
        sorting_function = choices["sorting_function"][sorting_function]
    except KeyError:
        logging.warning("Invalid sorting function specified, defaulting to 'lightness'.")
        sorting_function = choices["sorting_function"]["lightness"]
    sorted_pixels = sort_image(pixels, intervals, randomness, sorting_function)

    logging.debug("Placing pixels in output image...")
    output_img = util.place_pixels(sorted_pixels, mask_data, input_data, image.size)

    if angle is not 0:
        logging.debug("Rotating output image back to original orientation...")
        output_img = output_img.rotate(-angle, expand=True)

        logging.debug("Crop image to apropriate size...")
        output_img = util.crop_to(output_img, image)

    return output_img


def _main(args):
    output_path = args.pop("output_image_path")
    logging.debug("Opening image...")
    args["image"] = Image.open(args.pop("image_input_path"))
    mask_path = args.pop("mask_path")
    if mask_path:
        logging.debug("Opening mask...")
        args["mask_image"] = Image.open(mask_path)
    interval_file_path = args.pop("interval_file_path")
    if interval_file_path:
        logging.debug("Opening interval image...")
        args["interval_image"] = Image.open(interval_file_path)
    output_img = pixelsort(**args)
    logging.debug("Saving image...")
    output_img.save(output_path)

if __name__ == "__main__":
    _main(parse_args())
