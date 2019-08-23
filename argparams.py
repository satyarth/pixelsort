import argparse
import util
import interval
import sorting
import logging


def read_interval_function(int_function):
    try:
        return {
            "random": interval.random,
            "threshold": interval.threshold,
            "edges": interval.edge,
            "waves": interval.waves,
            "file": interval.file_mask,
            "file-edges": interval.file_edges,
            "none": interval.none
        }[int_function]
    except KeyError:
        logging.warning(
            "Invalid interval function specified, defaulting to 'threshold'.")
        return interval.threshold


def read_sorting_function(sorting_function):
    try:
        return {
            "lightness": sorting.lightness,
            "hue": sorting.hue,
            "intensity": sorting.intensity,
            "minimum": sorting.minimum,
            "saturation": sorting.saturation
        }[sorting_function]
    except KeyError:
        logging.warning(
            "Invalid sorting function specified, defaulting to 'lightness'.")
        return sorting.lightness


def parse_args():
    p = argparse.ArgumentParser(description="pixel mangle an image")
    p.add_argument("image", help="input image file")
    p.add_argument("-o", "--output", help="output image file, defaults to a randomly generated string",
                   default=util.id_generator() + ".png")
    p.add_argument("-i", "--int_function",
                   help="random, threshold, edges, waves, file, file-edges, none", default="threshold")
    p.add_argument("-f", "--int_file",
                   help="Image used for defining intervals", default="in.png")
    p.add_argument("-t", "--threshold", type=float,
                   help="Pixels darker than this are not sorted, between 0 and 1", default=0.25)
    p.add_argument("-u", "--upper_threshold", type=float,
                   help="Pixels brighter than this are not sorted, between 0 and 1", default=0.8)
    p.add_argument("-c", "--clength", type=int,
                   help="Characteristic length of random intervals", default=50)
    p.add_argument("-a", "--angle", type=float,
                   help="Rotate the image by an angle (in degrees) before sorting", default=0)
    p.add_argument("-r", "--randomness", type=float,
                   help="What percentage of intervals are NOT sorted", default=0)
    p.add_argument("-s", "--sorting_function",
                   help="lightness, intensity, hue, saturation, minimum", default="lightness")
    p.add_argument("-m", "--mask",
                   help="Image used for masking parts of the image")
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
        "bottom_threshold": __args.threshold,
        "upper_threshold": __args.upper_threshold,
        "clength": __args.clength,
        "angle": __args.angle,
        "randomness": __args.randomness,
        "sorting_function": __args.sorting_function,
        "mask": __args.mask
    }


def verify_args(args):
    # Informational logs
    logging.info(f"Interval function: {args['interval_function']}")
    if args["interval_function"] in ["threshold", "edges", "file-edges"]:
        logging.info(f"Lower threshold: {args['bottom_threshold']}")
    if args["interval_function"] == "threshold":
        logging.info(f"Upper threshold: {args['upper_threshold']}")
    if args["interval_function"] in ["random", "waves"]:
        logging.info(f"Characteristic length: {args['clength']}")
    logging.info(f"Randomness: {args['randomness']}%")
    # Actual validation
    if not args["output_image_path"]:
        output = f"{util.id_generator()}.png"
        logging.warning(
            f"No output path provided, defaulting to {output}")
        args["output_image_path"] = output
    args["interval_function"] = read_interval_function(
        args["interval_function"])
    args["sorting_function"] = read_sorting_function(args["sorting_function"])
