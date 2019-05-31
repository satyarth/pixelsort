try:
    import Image
except ImportError:
    from PIL import Image
from sorter import sort_image
from argparams import parse_args, verify_args
import util
import logging


def main(args):
    verify_args(args)

    logging.debug("Opening image...")
    input_img = Image.open(args["image_input_path"])

    logging.debug("Converting to RGBA...")
    input_img.convert('RGBA')

    logging.debug("Rotating image...")
    input_img = input_img.rotate(args["angle"], expand=True)

    logging.debug("Getting data...")
    data = input_img.load()

    logging.debug("Getting pixels...")
    pixels = []
    for y in range(input_img.size[1]):
        pixels.append([])
        for x in range(input_img.size[0]):
            pixels[y].append(data[x, y])

    logging.debug("Determining intervals...")
    intervals = args["interval_function"](pixels, args)

    logging.debug("Sorting pixels...")
    sorted_pixels = sort_image(
        pixels, intervals, args["randomness"], args["sorting_function"])

    logging.debug("Placing pixels in output image...")
    output_img = Image.new('RGBA', input_img.size)
    for y in range(output_img.size[1]):
        for x in range(output_img.size[0]):
            output_img.putpixel((x, y), sorted_pixels[y][x])

    if args["angle"] is not 0:
        logging.debug("Rotating output image back to original orientation...")
        output_img = output_img.rotate(-args["angle"], expand=True)

        logging.debug("Crop image to apropriate size...")
        output_img = util.crop_to(
            output_img, Image.open(args["image_input_path"]))

    logging.debug("Saving image...")
    output_img.save(args["output_image_path"])

    print(f"Done! {args['output_image_path']}")


if __name__ == "__main__":
    main(parse_args())
