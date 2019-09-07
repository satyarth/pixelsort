import argparse
import logging
from constants import defaults, choices
from util import id_generator

def parse_args():
    parser = argparse.ArgumentParser(description="Pixel mangle an image.")
    parser.add_argument("image", help="Input image file path.")
    parser.add_argument("-o", "--output",
                        help="Output image file path, defaults to the time created.",
                        default=id_generator() + ".png")
    parser.add_argument("-i", "--int_function",
                        choices=choices["interval_function"].keys(),
                        default=defaults["interval_function"],
                        help="Function to determine sorting intervals")
    parser.add_argument("-f", "--int_file", help="Image used for defining intervals.")
    parser.add_argument("-t", "--threshold", type=float, default=defaults["lower_threshold"],
                        help="Pixels darker than this are not sorted, between 0 and 1")
    parser.add_argument("-u", "--upper_threshold", type=float, default=defaults["upper_threshold"],
                        help="Pixels brighter than this are not sorted, between 0 and 1")
    parser.add_argument("-c", "--clength", type=int, default=defaults["clength"],
                        help="Characteristic length of random intervals")
    parser.add_argument("-a", "--angle", type=float, default=defaults["angle"],
                        help="Rotate the image by an angle (in degrees) before sorting")
    parser.add_argument("-r", "--randomness", type=float, default=defaults["randomness"],
                        help="What percentage of intervals are NOT sorted")
    parser.add_argument("-s", "--sorting_function",
                        choices=choices["sorting_function"].keys(),
                        default=defaults["sorting_function"],
                        help="Function to sort pixels by.")
    parser.add_argument("-m", "--mask", help="Image used for masking parts of the image")
    parser.add_argument("-l", "--log_level", default="WARNING", help="Print more or less info",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

    _args = parser.parse_args()

    logging.basicConfig(
        format="%(name)s: %(levelname)s - %(message)s", level=logging.getLevelName(_args.log_level))

    return {
        "image_input_path": _args.image,
        "output_image_path": _args.output,
        "interval_function": _args.int_function,
        "interval_file_path": _args.int_file,
        "lower_threshold": _args.threshold,
        "upper_threshold": _args.upper_threshold,
        "clength": _args.clength,
        "angle": _args.angle,
        "randomness": _args.randomness,
        "sorting_function": _args.sorting_function,
        "mask_path": _args.mask
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
