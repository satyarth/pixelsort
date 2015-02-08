from PIL import Image, ImageFilter
import random
import sys
import math
import argparse

p = argparse.ArgumentParser(description="pixel mangle an image")
p.add_argument("image", help="input image file")
p.add_argument("-o", "--output", help="output image file, defaults to output.png",default="output.png")
p.add_argument("-t", "--threshold", help="between 0 and 255*3",default=100)
p.add_argument("-r", "--randomness", help="what % of intervals are NOT sorted",default=0)
args = p.parse_args()

sys.setrecursionlimit(10000)
<<<<<<< HEAD
inputImage = 'image.jpg'
outputImage = "output.png"
threshold = 100 # Threshold for edge detection. Between 0 and 255*3
randomness = 30 # What % of intervals are NOT sorted

# End settings
=======
if args.output:
    outputImage = args.output
else:
    outputImage = "output.png"
>>>>>>> 338c3d4929638007b99dfc72cf6096aa0f2506ff

blackPixel = (0, 0, 0, 255)
whitePixel = (255, 255, 255, 255)

def quickSort(pixels):
	#Quicksort function that sorts pixels based on combined RGB values (R + B + G)
	if pixels == []:
		return pixels

	else:
		pivot = pixels[0]
		lesser = quickSort([x for x in pixels[1:] if (x[0] + x[1] + x[2]) < (pivot[0] + pivot[1] + pivot[2])])
		greater = quickSort([x for x in pixels[1:] if (x[0] + x[1] + x[2]) >= (pivot[0] + pivot[1] + pivot[2])])
		return lesser + [pivot] + greater


def randomWidth():
	# Defines the distribution of widths
	x = random.random()
	# width = int(200*(1-(1-(x-1)**2)**0.5))
	width = int(50*(1-x))
<<<<<<< HEAD
	# width = int(50/(x+0.1))
=======
>>>>>>> 338c3d4929638007b99dfc72cf6096aa0f2506ff
	return(width)

def selectiveSort(pixels,filterPixels):
	sortedPixels = []
	edgePixels = []
	intervals = []

	print("Thresholding...")
	for y in range(len(pixels)):
		edgePixels.append([])
		for x in range(len(pixels[0])):
<<<<<<< HEAD
			if filterPixels[y][x][0] + filterPixels[y][x][1] + filterPixels[y][x][2] < threshold:
=======
			if filterPixels[y][x][0] + filterPixels[y][x][1] + filterPixels[y][x][2] < args.threshold:
>>>>>>> 338c3d4929638007b99dfc72cf6096aa0f2506ff
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
			if random.randint(0,100)>=args.randomness:
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
			if random.randint(0,100)>=args.randomness:
				row=row+quickSort(interval)
			else:
				row=row+interval
			xMin = xMax
		row.append(pixels[y][0]) # wat
		sortedPixels.append(row)
	return(sortedPixels)

def pixelSort():
	print("Opening image...")
<<<<<<< HEAD
	img = Image.open(inputImage)
=======
	img = Image.open(args.image)
>>>>>>> 338c3d4929638007b99dfc72cf6096aa0f2506ff
	edges = img.filter(ImageFilter.FIND_EDGES)
	img = img.convert('RGBA')
	edges = edges.convert('RGBA')

	print("Get data...")
	data = img.load()
	edgeData = edges.load()
	new = Image.new('RGBA', img.size)

	pixels = []
	filterPixels = []
	intervals = []
	print("Getting pixels...")
	#Load all of the pixels into the pixels list
	for y in range(img.size[1]):
		filterPixels.append([])
		pixels.append([])
		for x in range(img.size[0]):
			filterPixels[y].append(edgeData[x, y])
			pixels[y].append(data[x, y])

	sortedPixels = randomSort(pixels)
	# sortedPixels = selectiveSort(pixels, filterPixels)

	print("Placing pixels...")
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			new.putpixel((x, y), sortedPixels[y][x]) #apply the pixels to the new image

	print("Saving image...")
	new.save(outputImage)	


<<<<<<< HEAD
pixelSort()
=======
pixelSort()
>>>>>>> 338c3d4929638007b99dfc72cf6096aa0f2506ff
