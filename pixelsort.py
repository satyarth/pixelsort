try:
    import Image
except ImportError:
    from PIL import Image
import sorter
import argparams
import util


def main():
    print("Opening image...")
    input_img = Image.open(argparams.image_input_path)

    print("Converting to RGBA...")
    input_img.convert('RGBA')

    print("Rotating image...")
    input_img = input_img.rotate(argparams.angle, expand=True)

    print("Getting data...")
    data = input_img.load()

    print("Getting pixels...")
    pixels = []
    for y in range(input_img.size[1]):
        pixels.append([])
        for x in range(input_img.size[0]):
            pixels[y].append(data[x, y])

    print("Determining intervals...")
    intervals = argparams.interval_function(pixels, argparams)

    print("Sorting pixels...")
    sorted_pixels = sorter.sort_image(pixels, intervals, argparams)

    print("Placing pixels in output image...")
    output_img = Image.new('RGBA', input_img.size)
    for y in range(output_img.size[1]):
        for x in range(output_img.size[0]):
            output_img.putpixel((x, y), sorted_pixels[y][x])

    if argparams.angle is not 0:
        print("Rotating output image back to original orientation...")
        output_img = output_img.rotate(-argparams.angle, expand=True)

        print("Crop image to apropriate size...")
        output_img = util.crop_to(output_img, Image.open(argparams.image_input_path))

    print("Saving image...")
    output_img.save(argparams.output_image_path)

    print("Done!", argparams.output_image_path)


if __name__ == "__main__":
    main()
