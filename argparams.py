import argparse
import logging
from constants import defaults, choices
from util import id_generator

def parse_args():
    p = argparse.ArgumentParser(description="Pixel mangle an image.")
    p.add_argument("image", help="Input image file path.")
    p.add_argument("-o", "--output", help="Output image file path, defaults to the time created.",
                   default=id_generator() + ".png")
    p.add_argument("-i", "--int_function",
                   choices=choices["interval_function"].keys(),
                   default=defaults["interval_function"],
                   help="Function to determine sorting intervals")
    p.add_argument("-f", "--int_file", help="Image used for defining intervals.")
    p.add_argument("-t", "--threshold", type=float, default=defaults["lower_threshold"],
                   help="Pixels darker than this are not sorted, between 0 and 1")
    p.add_argument("-u", "--upper_threshold", type=float, default=defaults["upper_threshold"],
                   help="Pixels brighter than this are not sorted, between 0 and 1")
    p.add_argument("-c", "--clength", type=int, default=defaults["clength"],
                   help="Characteristic length of random intervals")
    p.add_argument("-a", "--angle", type=float, default=defaults["angle"],
                   help="Rotate the image by an angle (in degrees) before sorting")
    p.add_argument("-r", "--randomness", type=float, default=defaults["randomness"],
                   help="What percentage of intervals are NOT sorted")
    p.add_argument("-s", "--sorting_function",
                   choices=choices["sorting_function"].keys(),
                   default=defaults["sorting_function"],
                   help="Function to sort pixels by.")
    p.add_argument("-m", "--mask", help="Image used for masking parts of the image")
    p.add_argument("-l", "--log_level", default="WARNING", help="Print more or less info",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

    __args = p.parse_args()

    logging.basicConfig(
        format="%(name)s: %(levelname)s - %(message)s", level=logging.getLevelName(__args.log_level))

    return {
        "image_input_path": __args.image,
        "output_image_path": __args.output,
        "interval_function": __args.int_function,
        "interval_file_path": __args.int_file,
        "lower_threshold": __args.threshold,
        "upper_threshold": __args.upper_threshold,
        "clength": __args.clength,
        "angle": __args.angle,
        "randomness": __args.randomness,
        "sorting_function": __args.sorting_function,
        "mask_path": __args.mask
    }


def verify_args(args):
    # Informational logs
    logging.info("Interval function: {}".format(args['interval_function']))
    if args["interval_function"] in ["threshold", "edges", "file-edges"]:
        logging.info("Lower threshold: {}".format(args['bottom_threshold']))
    if args["interval_function"] == "threshold":
        logging.info("Upper threshold: {}".format(args['upper_threshold']))
    if args["interval_function"] in ["random", "waves"]:
        logging.info("Characteristic length: {}".format(args['clength']))
    logging.info("Randomness: {}".format(args['randomness']))
    # Actual validation
    if not args["output_image_path"]:
        output = "{}.png".format(util.id_generator())
        logging.warning(
            "No output path provided, defaulting to {}".format(output))
        args["output_image_path"] = output
    args["interval_function"] = read_interval_function(
        args["interval_function"])
    args["sorting_function"] = read_sorting_function(args["sorting_function"])
