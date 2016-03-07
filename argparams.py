import argparse
import util
import interval
import sorting


def read_output_image_path():
    return __args.output if __args.output else util.id_generator() + ".png"


def read_interval_function():
    try:
        return {
            "random": interval.random,
            "threshold": interval.threshold,
            "edges": interval.edge,
            "waves": interval.waves,
            "file": interval.file_mask,
            "file-edges": interval.file_edges,
            "none": interval.none}[__args.int_function]
    except KeyError:
        print("[WARNING] Invalid interval function specified, defaulting to 'threshold'.")
        return interval.threshold


def read_sorting_function():
    try:
        return {
            "lightness": sorting.lightness,
            "intensity": sorting.intensity,
            "maximum": sorting.maximum,
            "minimum": sorting.minimum
            }[__args.sorting_function]
    except KeyError:
        print("[WARNING] Invalid sorting function specified, defaulting to 'lightness'.")
        return sorting.lightness


p = argparse.ArgumentParser(description="pixel mangle an image")
p.add_argument("image", help="input image file")
p.add_argument("-o", "--output", help="output image file, defaults to a randomly generated string")
p.add_argument("-i", "--int_function", help="random, threshold, edges, waves, file, file-edges, none", default="threshold")
p.add_argument("-f", "--int_file", help="Image used for defining intervals", default="in.png")
p.add_argument("-t", "--threshold", type=float, help="Pixels darker than this are not sorted, between 0 and 1", default=0.25)
p.add_argument("-u", "--upper_threshold", type=float, help="Pixels darker than this are not sorted, between 0 and 1", default=0.8)
p.add_argument("-c", "--clength", type=int, help="Characteristic length of random intervals", default=50)
p.add_argument("-a", "--angle", type=float, help="Rotate the image by an angle (in degrees) before sorting", default=0)
p.add_argument("-r", "--randomness", type=float, help="What percentage of intervals are NOT sorted", default=0)
p.add_argument("-s", "--sorting_function", help="lightness, intensity, maximum, minimum", default="lightness")
__args = p.parse_args()

image_input_path = __args.image
output_image_path = read_output_image_path()
interval_function = read_interval_function()
interval_file_path = __args.int_file
bottom_threshold = __args.threshold
upper_threshold = __args.upper_threshold
clength = __args.clength
angle = __args.angle
randomness = __args.randomness
sorting_function = read_sorting_function()

print("Interval function: ", __args.int_function)
if __args.int_function in ["threshold", "edges", "file-edges"]:
    print("Lower threshold: ", __args.threshold)
if __args.int_function == "threshold":
    print("Upper threshold: ", __args.upper_threshold)
if __args.int_function in ["random", "waves"]:
    print("Characteristic length: ", __args.clength)
print("Randomness: ", __args.randomness, "%")
