import os
from PIL import Image
import logging
from pixelsort.argparams import parse_args
from pixelsort.main import pixelsort
from pixelsort.util import id_generator

args = parse_args()
image_input_path = args.pop("image_input_path")
image_output_path = args.pop("image_output_path")
interval_file_path = args.pop("interval_file_path")
mask_path = args.pop("mask_path")

if image_output_path is None:
    if not os.path.exists("out/"):
        os.mkdir("out/")
    extension = os.path.splitext(image_input_path)[1] or ".png"
    image_output_path = f"out/{id_generator()}{extension}"
    logging.warning("No output path provided, using " + image_output_path)

logging.debug("Opening image...")
args["image"] = Image.open(image_input_path)
if mask_path:
    logging.debug("Opening mask...")
    args["mask_image"] = Image.open(mask_path)
if interval_file_path:
    logging.debug("Opening interval file...")
    args["interval_image"] = Image.open(interval_file_path)

image = pixelsort(**args)
logging.debug("Saving image...")
if os.path.splitext(image_output_path)[1].lower() in (".jpg", ".jpeg"):
    # JPEG has no alpha channel
    image = image.convert("RGB")
image.save(image_output_path)
