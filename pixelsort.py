from PIL import Image, ImageFilter
import random
import string
import sys
import math
import argparse

p = argparse.ArgumentParser(description="pixel mangle an image")
p.add_argument("image", help="input image file")
p.add_argument("-o", "--output", help="output image file, defaults to %input%-sorted.png")
p.add_argument("-t", "--threshold", help="between 0 and 255*3",default=100)
p.add_argument("-c", "--clength", help="characteristic length",default=50)
p.add_argument("-r", "--randomness", help="what % of intervals are NOT sorted",default=0)
args = p.parse_args()

randomness = int(args.randomness)
threshold = int(args.threshold)
clength = int(args.clength)

print "Randomness =", randomness, "%"
print "Threshold =", threshold
print "Characteristic length = ", clength

blackPixel = (0, 0, 0, 255)
whitePixel = (255, 255, 255, 255)

def id_generator(size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

if args.output:
    outputImage = args.output
else:
    outputImage = id_generator()+".png"

def quickSort(pixels):
	if pixels == []:
		return []
	elif isinstance(pixels[0], tuple):
		return(sorted(pixels, key = lambda x: x[0] + x[1] + x[2]))
	else:
		return(sorted(pixels))

def randomWidth():
	# Defines the distribution of widths in randomSort
	x = random.random()
	# width = int(200*(1-(1-(x-1)**2)**0.5))
	width = int(clength*(1-x))
	# width = int(50/(x+0.1))
	return(width)

def selectiveSort(pixels):
	img = Image.open(args.image)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edgeData = edges.load()

	filterPixels = []
	sortedPixels = []
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

	print("Sorting intervals...")
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

def randomSort(pixels):
	sortedPixels = []
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

	print("Sorting intervals...")
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

def rgbSort(pixels, sortFunction):
	# Splits image into channels, then applies sortFunction to each channel separately
	sortedPixels = []
	intervals = []
	# Separate pixels into channels
	channels = []
	for channel in [0, 1, 2]:
		channels.append([])
		for y in range(len(pixels)):
			channels[channel].append([])
			for x in range(len(pixels[0])):
				channels[channel][y].append(pixels[y][x][channel])

	# randomSort the channels separately
	for channel in [0, 1, 2]:
		channels[channel] = sortFunction(channels[channel])
	for y in range(len(pixels)):
		sortedPixels.append([])
		for x in range(len(pixels[0])):
			sortedPixels[y].append((channels[0][y][x], channels[1][y][x], channels[2][y][x], 255))
	return(sortedPixels)

def pixelSort():
	print("Opening image...")
	img = Image.open(args.image)
	img = img.convert('RGBA')

	print("Get data...")
	data = img.load()
	new = Image.new('RGBA', img.size)

	pixels = []
	channels = []

	print("Getting pixels...")
	for y in range(img.size[1]):
		pixels.append([])
		for x in range(img.size[0]):
			pixels[y].append(data[x, y])

	#sortedPixels = rgbSort(pixels, randomSort)
	#sortedPixels = rgbSort(pixels, selectiveSort)
	sortedPixels = randomSort(pixels)
	#sortedPixels = selectiveSort(pixels)
	print("Placing pixels...")
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			new.putpixel((x, y), sortedPixels[y][x]) #apply the pixels to the new image

	print("Saving image...")
	new.save(outputImage)
	print "Done!", outputImage

pixelSort()
