try:
    import Image
except ImportError:
    from PIL import Image
from sorter import sort_image
from argparams import parse_args, verify_args
import util
import constants


def main(args):
    verify_args(args)

    print("Opening image...")
    input_img = Image.open(args["image_input_path"])

    print("Converting to RGBA...")
    input_img.convert('RGBA')

    print("Rotating image...")
    input_img = input_img.rotate(args["angle"], expand=True)

    print("Getting data...")
    data = input_img.load()

    print("Loading mask...")
    mask = Image.open(args["mask"]).convert(
        'RGBA').load() if args["mask"] else None

    print("Getting pixels...")
    pixels = get_pixels(data, mask, input_img.size)

    print("Determining intervals...")
    intervals = args["interval_function"](pixels, args)
    print("Sorting pixels...")
    sorted_pixels = sort_image(
        pixels, intervals, args["randomness"], args["sorting_function"])

    print("Placing pixels in output image...")
    output_img = place_pixels(sorted_pixels, mask, data, input_img.size)

    if args["angle"] is not 0:
        print("Rotating output image back to original orientation...")
        output_img = output_img.rotate(-args["angle"], expand=True)

        print("Crop image to apropriate size...")
        output_img = util.crop_to(
            output_img, Image.open(args["image_input_path"]))

    print("Saving image...")
    output_img.save(args["output_image_path"])

    print("Done!", args["output_image_path"])


def get_pixels(data, mask, size):
    pixels = []
    for y in range(size[1]):
        pixels.append([])
        for x in range(size[0]):
            if not (mask and mask[x, y] == constants.black_pixel):
                pixels[y].append(data[x, y])
    return pixels


def place_pixels(pixels, mask, original, size):
    output_img = Image.new('RGBA', size)
    for y in range(size[1]):
        count = 0
        for x in range(size[0]):
            if mask and mask[x, y] == constants.black_pixel:
                output_img.putpixel((x, y), original[x, y])
            else:
                output_img.putpixel((x, y), pixels[y][count])
                count += 1
    return output_img


if __name__ == "__main__":
    main(parse_args())
