# pixelsort

### What is Pixel Sorting?

Have a look at [this post](http://satyarth.me/articles/pixel-sorting/) or [/r/pixelsorting](http://www.reddit.com/r/pixelsorting/top/)

### How this program works:

The interval function (selected via command line, `random` by default) partitions each row of the image into intervals and returns an array `intervals` that defines them. This array, along with the image (in RGB array form) are passed to `sort_image` which does the dirty work and returns an array of sorted pixels.

### Usage
```
git clone https://github.com/satyarth/pixelsort.git
cd pixelsort
python3 pixelsort.py %PathToImage% [options]
```
####Parameters (Command Line):

* **`-i` (interval function):** Controls how the intervals used for sorting are defined. 

* **`-o` (output file):** Path of output file. Randomly generates a file name by default.

* **`-r` (randomness):** What % of intervals *not* to sort. 0 by default.

* **`-t` (threshold):** Defines the threshold while performing edge detection. `100` by default.

* **`-c` (clength):** Characteristic length for the random width generator.

* **`-a` (angle):** Angle at which you're pixel sorting. `0` (horizontal) by default.

* **`-f` (intervals file):** Image used to define intervals.

#### Interval Functions

* `random`: Randomly generate intervals. Distribution of widths is linear by default. Interval widths can be scaled using `clength`.

`python3 pixelsort.py examples/image.jpg -i random -c 20`

![random](/examples/random.png)

* `edges`: Performs an edge detection, which is used to define intervals. Tweak threshold with `threshold`.

`python3 pixelsort.py examples/image.jpg -i edges -t 250`

![edges](/examples/edges.png)

* `none`: Intervals = entire rows.

`python3 pixelsort.py examples/image.jpg -i none`

![none](/examples/none.png)

* `waves`: Intervals are waves of nearly uniform widths. Control width of waves with `clength`.

`python3 pixelsort.py examples/image.jpg -i waves`

![none](/examples/waves.png)

* `file`: Intervals taken from image specified with `-f`. Must be black and white and the same size as the input image.

`python3 pixelsort.py examples/image.jpg -i file -f examples/intervals.png `

![file](/examples/intervals.png)

(generated with [elementary-ca](https://github.com/satyarth/elementary-ca))

![file](/examples/file.png)

### todo

* Allow defining different intervals for different channels.
* Sorting along arbitrary functions

---

Based on https://gist.github.com/LycaonIsAWolf/667c5554e5d9d9a25ae6