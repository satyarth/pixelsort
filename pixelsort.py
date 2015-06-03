try:
	import Image, ImageFilter
except ImportError:
	from PIL import Image, ImageFilter
import random
import string
import argparse

p = argparse.ArgumentParser(description = "pixel mangle an image")
p.add_argument("image", help = "input image file")
p.add_argument("-o", "--output", help = "output image file, defaults to a randomly generated string")
p.add_argument("-i", "--int_function", help = "random, edges, waves, file, none", default = "random")
p.add_argument("-f", "--int_file", help = "image for intervals", default = "in.png")
p.add_argument("-t", "--threshold", help = "between 0 and 255*3", default = 100)
p.add_argument("-c", "--clength", help = "characteristic length", default = 50)
p.add_argument("-a", "--angle", help = "rotate the image by an angle before sorting", default = 0)
p.add_argument("-r", "--randomness", help = "what % of intervals are NOT sorted", default = 0)
args = p.parse_args()

randomness = int(args.randomness)
threshold = int(args.threshold)
clength = int(args.clength)
angle = float(args.angle)

print("Randomness =", randomness, "%")
print("Threshold =", threshold)
print("Characteristic length = ", clength)

black_pixel = (0, 0, 0, 255)
white_pixel = (255, 255, 255, 255)

# Generates names for output files
def id_generator(size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

if args.output:
	outputImage = args.output
else:
	outputImage = id_generator()+".png"

# Sorts a given row of pixels
def sort_interval(interval):
	if interval == []:
		return []
	else:
		return(sorted(interval, key = lambda x: x[0] + x[1] + x[2]))

# Generates random widths for intervals. Used by int_random()
def random_width():
	x = random.random()
	# width = int(200*(1-(1-(x-1)**2)**0.5))
	width = int(clength*(1-x))
	# width = int(50/(x+0.1))
	return(width)

# Functions starting with int return intervals according to which to sort
def int_edges(pixels):
	img = Image.open(args.image)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edge_data = edges.load()

	filter_pixels = []
	edge_pixels = []
	intervals = []

	print("Defining edges...")
	for y in range(img.size[1]):
		filter_pixels.append([])
		for x in range(img.size[0]):
			filter_pixels[y].append(edge_data[x, y])

	print("Thresholding...")
	for y in range(len(pixels)):
		edge_pixels.append([])
		for x in range(len(pixels[0])):
			if filter_pixels[y][x][0] + filter_pixels[y][x][1] + filter_pixels[y][x][2] < threshold:
				edge_pixels[y].append(white_pixel)
			else:
				edge_pixels[y].append(black_pixel)

	print("Cleaning up edges...")
	for y in range(len(pixels)-1,1,-1):
		for x in range(len(pixels[0])-1,1,-1):
			if edge_pixels[y][x] == black_pixel and edge_pixels[y][x-1] == black_pixel:
				edge_pixels[y][x] = white_pixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if edge_pixels[y][x] == black_pixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return(intervals)

def int_random(pixels):
	intervals = []

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		x = 0
		while True:
			width = random_width()
			x += width
			if x > len(pixels[0]):
				intervals[y].append(len(pixels[0]))
				break
			else:
				intervals[y].append(x)
	return(intervals)

def int_waves(pixels):
	intervals = []

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		x = 0
		while True:
			width = clength + random.randint(0,10)
			x += width
			if x > len(pixels[0]):
				intervals[y].append(len(pixels[0]))
				break
			else:
				intervals[y].append(x)
	return(intervals)

def int_file(pixels):
	intervals = []
	file_pixels = []

	img = Image.open(args.int_file)
	img = img.convert('RGBA')
	data = img.load()
	for y in range(img.size[1]):
		file_pixels.append([])
		for x in range(img.size[0]):
			file_pixels[y].append(data[x, y])

	print("Cleaning up edges...")
	for y in range(len(pixels)-1,1,-1):
		for x in range(len(pixels[0])-1,1,-1):
			if file_pixels[y][x] == black_pixel and file_pixels[y][x-1] == black_pixel:
				file_pixels[y][x] = white_pixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if file_pixels[y][x] == black_pixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))

	return intervals

def int_file_edges(pixels):
	img = Image.open(args.int_file)
	img = img.resize((len(pixels[0]), len(pixels)), Image.ANTIALIAS)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edge_data = edges.load()

	filter_pixels = []
	edge_pixels = []
	intervals = []

	print("Defining edges...")
	for y in range(img.size[1]):
		filter_pixels.append([])
		for x in range(img.size[0]):
			filter_pixels[y].append(edge_data[x, y])

	print("Thresholding...")
	for y in range(len(pixels)):
		edge_pixels.append([])
		for x in range(len(pixels[0])):
			if filter_pixels[y][x][0] + filter_pixels[y][x][1] + filter_pixels[y][x][2] < threshold:
				edge_pixels[y].append(white_pixel)
			else:
				edge_pixels[y].append(black_pixel)

	print("Cleaning up edges...")
	for y in range(len(pixels)-1,1,-1):
		for x in range(len(pixels[0])-1,1,-1):
			if edge_pixels[y][x] == black_pixel and edge_pixels[y][x-1] == black_pixel:
				edge_pixels[y][x] = white_pixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if edge_pixels[y][x] == black_pixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return(intervals)

def int_none(pixels):
	intervals = []
	for y in range(len(pixels)):
		intervals.append([len(pixels[y])])
	return(intervals)

# Get function to define intervals from command line arguments
try:	
	int_function = {
		"random": int_random,
		"edges": int_edges,
		"waves": int_waves,
		"file": int_file,
		"file-edges": int_file_edges,
		"none": int_none}[args.int_function]
except KeyError:
	print("[WARNING] Invalid interval function specified, defaulting to 'random'. Try one of [random, edges, waves, file, none]")
	int_function = int_random

# Sorts the image
def sort_image(pixels, intervals):
	print("Sorting intervals...")
	# Hold sorted pixels
	sorted_pixels=[]
	for y in range(len(pixels)):
		row=[]
		xMin = 0
		for xMax in intervals[y]:
			interval = []
			for x in range(xMin, xMax):
				interval.append(pixels[y][x])
			if random.randint(0,100) >= randomness:
				row = row + sort_interval(interval)
			else:
				row = row + interval
			xMin = xMax
		row.append(pixels[y][0]) # wat
		sorted_pixels.append(row)
	return(sorted_pixels)

def pixel_sort():
	print("Opening image...")
	img = Image.open(args.image)
	img.convert('RGBA')
	img = img.rotate(angle, expand = True)

	print("Getting data...")
	data = img.load()
	new = Image.new('RGBA', img.size)

	pixels = []

	print("Getting pixels...")
	for y in range(img.size[1]):
		pixels.append([])
		for x in range(img.size[0]):
			pixels[y].append(data[x, y])

	intervals = int_function(pixels)
	sorted_pixels = sort_image(pixels, intervals)

	print("Placing pixels...")
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			new.putpixel((x, y), sorted_pixels[y][x])

	new = new.rotate(-angle)
	print("Saving image...")
	new.save(outputImage)
	print("Done!", outputImage)

pixel_sort()
