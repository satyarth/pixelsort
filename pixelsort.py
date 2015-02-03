from PIL import Image, ImageFilter
import random, sys

# Settings

sys.setrecursionlimit(10000)
threshold = 50 # Threshold for edge detection. Between 0 and 255*3
randomness = 50 # What % of intervals are NOT sorted

print "Threshold:", threshold
print "Randomness:", randomness

inputImage = 'image.jpg'
outputImage = str(sys.argv[1])+".png"

# End settings

blackPixel = (0, 0, 0, 255)
whitePixel = (255, 255, 255, 255)

def quick_sort(pixels):
	#Quicksort function that sorts pixels based on combined RGB values (R + B + G)
	if pixels == []:
		return pixels

	else:
		pivot = pixels[0]
		lesser = quick_sort([x for x in pixels[1:] if (x[0] + x[1] + x[2]) < (pivot[0] + pivot[1] + pivot[2])])
		greater = quick_sort([x for x in pixels[1:] if (x[0] + x[1] + x[2]) >= (pivot[0] + pivot[1] + pivot[2])])
		return lesser + [pivot] + greater


def sort_all_pixels():
	#sorts every line of pixels
	print("Sorting all pixels.")

	print("Opening image...")
	img = Image.open(inputImage)
	edges = img.filter(ImageFilter.FIND_EDGES)
	img = img.convert('RGBA')
	edges = edges.convert('RGBA')

	print("Get data...")
	data = img.load()
	edgeData = edges.load()

	new = Image.new('RGBA', img.size)

	pixels = []
	sorted_pixels = []
	filterPixels = []
	edgePixels = []
	intervals = []
	print("Getting pixels...")
	#Load all of the pixels into the pixels list
	for y in range(img.size[1]):
		filterPixels.append([])
		pixels.append([])
		for x in range(img.size[0]):
			filterPixels[y].append(edgeData[x, y])
			pixels[y].append(data[x, y])

	print("Thresholding...")
	for y in range(img.size[1]):
		edgePixels.append([])
		for x in range(img.size[0]):
			if filterPixels[y][x][0] + filterPixels[y][x][1] + filterPixels[y][x][2] < threshold:
				edgePixels[y].append(whitePixel)
			else:
				edgePixels[y].append(blackPixel)

	print("Cleaning up edges...")
	for y in range(img.size[1]-1,1,-1):
		for x in range(img.size[0]-1,1,-1):
			if edgePixels[y][x] == blackPixel and edgePixels[y][x-1] == blackPixel:
				edgePixels[y][x] = whitePixel

	print("Defining intervals...")
	for y in range(img.size[1]):
		intervals.append([])
		for x in range(img.size[0]):
			if edgePixels[y][x] == blackPixel:
				intervals[y].append(x)
		intervals[y].append(img.size[0])

	print("Sorting intervals...")
	test=[]
	for y in range(img.size[1]):
		row=[]
		xMin = 0
		for xMax in intervals[y]:
			interval = []
			for x in range(xMin, xMax):
				interval.append(pixels[y][x])
			if random.randint(0,100)>=randomness:
				row=row+quick_sort(interval)
			else:
				row=row+interval
			xMin = xMax
		row.append(pixels[y][0]) # wat
		test.append(row)


	print("Placing pixels...")
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			new.putpixel((x, y), test[y][x]) #apply the pixels to the new image

	print("Saving image...")
	new.save(outputImage)

sort_all_pixels()