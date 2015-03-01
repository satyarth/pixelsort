from PIL import Image, ImageFilter
import random
import string
import sys
import math
import argparse

p = argparse.ArgumentParser(description="pixel mangle an image")
p.add_argument("image", help="input image file")
p.add_argument("-o", "--output", help="output image file, defaults to %input%-sorted.png")
p.add_argument("-i", "--intFunction", help="random, edges, waves, file, none",default="random")
p.add_argument("-f", "--intfile", help="image for intervals",default="in.png")
p.add_argument("-t", "--threshold", help="between 0 and 255*3",default=100)
p.add_argument("-c", "--clength", help="characteristic length",default=50)
p.add_argument("-r", "--randomness", help="what % of intervals are NOT sorted",default=0)
p.add_argument("-m", "--multichannel", help="'y' enables multichannel mode",default='n')
args = p.parse_args()

randomness = int(args.randomness)
threshold = int(args.threshold)
clength = int(args.clength)

print "Randomness =", randomness, "%"
print "Threshold =", threshold
print "Characteristic length = ", clength

blackPixel = (0, 0, 0, 255)
whitePixel = (255, 255, 255, 255)

# Generates names for output files
def id_generator(size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

if args.output:
    outputImage = args.output
else:
    outputImage = id_generator()+".png"

# Sorts a given row of pixels, can handle individual channels as well
def quickSort(pixels):
	if pixels == []:
		return []
	elif isinstance(pixels[0], tuple):
		return(sorted(pixels, key = lambda x: x[0] + x[1] + x[2]))
	else:
		return(sorted(pixels, key = lambda x: x))

# Generates random widths for intervals. Used by intRandom()
def randomWidth():
	x = random.random()
	# width = int(200*(1-(1-(x-1)**2)**0.5))
	width = int(clength*(1-x))
	# width = int(50/(x+0.1))
	return(width)

# Functions starting with int return intervals according to which to sort
def intEdges(pixels):
	img = Image.open(args.image)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edgeData = edges.load()

	filterPixels = []
	edgePixels = []
	intervals = []

	print("Defining edges...")
	for y in range(img.size[1]):
		filterPixels.append([])
		for x in range(img.size[0]):
			filterPixels[y].append(edgeData[x, y])

	print("Thresholding...")
	for y in range(len(pixels)):
		edgePixels.append([])
		for x in range(len(pixels[0])):
			if filterPixels[y][x][0] + filterPixels[y][x][1] + filterPixels[y][x][2] < threshold:
				edgePixels[y].append(whitePixel)
			else:
				edgePixels[y].append(blackPixel)

	print("Cleaning up edges...")
	for y in range(len(pixels)-1,1,-1):
		for x in range(len(pixels[0])-1,1,-1):
			if edgePixels[y][x] == blackPixel and edgePixels[y][x-1] == blackPixel:
				edgePixels[y][x] = whitePixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if edgePixels[y][x] == blackPixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return(intervals)

def intRandom(pixels):
	intervals = []

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		x = 0
		while True:
			width = randomWidth()
			x += width
			if x > len(pixels[0]):
				intervals[y].append(len(pixels[0]))
				break
			else:
				intervals[y].append(x)
	return(intervals)

def intWaves(pixels):
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

def intFile(pixels):
	intervals = []
	filePixels = []

	img = Image.open(args.intfile)
	img = img.convert('RGBA')
	data = img.load()
	for y in range(img.size[1]):
		filePixels.append([])
		for x in range(img.size[0]):
			filePixels[y].append(data[x, y])

	print("Cleaning up edges...")
	for y in range(len(pixels)-1,1,-1):
		for x in range(len(pixels[0])-1,1,-1):
			if filePixels[y][x] == blackPixel and filePixels[y][x-1] == blackPixel:
				filePixels[y][x] = whitePixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if filePixels[y][x] == blackPixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))

	return intervals

def intFileEdges(pixels):
	img = Image.open(args.intfile)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edgeData = edges.load()

	filterPixels = []
	edgePixels = []
	intervals = []

	print("Defining edges...")
	for y in range(img.size[1]):
		filterPixels.append([])
		for x in range(img.size[0]):
			filterPixels[y].append(edgeData[x, y])

	print("Thresholding...")
	for y in range(len(pixels)):
		edgePixels.append([])
		for x in range(len(pixels[0])):
			if filterPixels[y][x][0] + filterPixels[y][x][1] + filterPixels[y][x][2] < threshold:
				edgePixels[y].append(whitePixel)
			else:
				edgePixels[y].append(blackPixel)

	print("Cleaning up edges...")
	for y in range(len(pixels)-1,1,-1):
		for x in range(len(pixels[0])-1,1,-1):
			if edgePixels[y][x] == blackPixel and edgePixels[y][x-1] == blackPixel:
				edgePixels[y][x] = whitePixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if edgePixels[y][x] == blackPixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return(intervals)

def intNone(pixels):
	intervals = []
	for y in range(len(pixels)):
		intervals.append([len(pixels[0])])
	return(intervals)

# Defining intervals from command line arguments
if args.intFunction == "random":
	intFunction = intRandom
elif args.intFunction == "edges":
	intFunction = intEdges
elif args.intFunction == "waves":
	intFunction = intWaves
elif args.intFunction == "file":
	intFunction = intFile
elif args.intFunction == "file-edges":
	intFunction = intFileEdges
elif args.intFunction == "none":
	intFunction = intNone
else:
	print "Error! Invalid interval function."

# Sorts each channel separately
def sortPixelsMultichannel(pixels, intervalses):
	sortedPixels = []
	# Separate pixels into channels
	channels = []
	for channel in [0, 1, 2]:
		channels.append([])
		for y in range(len(pixels)):
			channels[channel].append([])
			for x in range(len(pixels[0])):
				channels[channel][y].append(pixels[y][x][channel])

	# sort the channels separately
	for channel in [0, 1, 2]:
		channels[channel] = sortPixels(channels[channel],intervalses[channel])
	for y in range(len(pixels)):
		sortedPixels.append([])
		for x in range(len(pixels[0])):
			sortedPixels[y].append((channels[0][y][x], channels[1][y][x], channels[2][y][x], 255))
	return(sortedPixels)

# Sorts the image
def sortPixels(pixels, intervals):
	print("Sorting intervals...")
	# Hold sorted pixels
	sortedPixels=[]
	for y in range(len(pixels)):
		row=[]
		xMin = 0
		for xMax in intervals[y]:
			interval = []
			for x in range(xMin, xMax):
				interval.append(pixels[y][x])
			if random.randint(0,100)>=randomness:
				row=row+quickSort(interval)
			else:
				row=row+interval
			xMin = xMax
		row.append(pixels[y][0]) # wat
		sortedPixels.append(row)
	return(sortedPixels)

def pixelSort():
	print("Opening image...")
	img = Image.open(args.image)
	img = img.convert('RGBA')

	print("Getting data...")
	data = img.load()
	new = Image.new('RGBA', img.size)

	pixels = []

	print("Getting pixels...")
	for y in range(img.size[1]):
		pixels.append([])
		for x in range(img.size[0]):
			pixels[y].append(data[x, y])

	if args.multichannel == 'y': # If multichannel mode is enabled
		intervalses = []		 # intervalses: List of intervals
		for channel in [0, 1, 2]:
			intervalses.append(intRandom(pixels))
		sortedPixels = sortPixelsMultichannel(pixels, intervalses)
	else:
		intervals = intFunction(pixels)
		sortedPixels = sortPixels(pixels, intervals)

	print("Placing pixels...")
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			new.putpixel((x, y), sortedPixels[y][x])

	print("Saving image...")
	new.save(outputImage)
	print "Done!", outputImage

pixelSort()
