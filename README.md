# pixelsort

### What is Pixel Sorting?

Have a look at [this post](http://satyarth.me/articles/pixel-sorting/) or [/r/pixelsorting](http://www.reddit.com/r/pixelsorting/top/)

### How this program works:

The interval function (selected via command line, `random` by default) partitions each row of the image into intervals and returns an array `intervals` that defines them. This array, along with the image (in RGB array form) are passed to `sortPixels` which does the dirty work and returns an array of sorted pixels.

*Multichannel mode:* used to sort the pixels in each color channel separately.

### Usage
```
git clone https://github.com/accden/pixelsort.git
cd pixelsort
python pixelsort.py /path/to/input/file.jpg -i [interval function] -m [multichannel] -o [output] -r [randomness] -t [threshold] -c [clength]
```
####Parameters:

* **`i`(interval function):** Controls how the intervals used for sorting are defined. Options:

1. `random`(default): Uniform random widths
Examples: http://a.pomf.se/yvadry.png http://a.pomf.se/sckkfy.png

2. `edges`: Defined by edges in the image. Can control via threshold.
Examples: http://a.pomf.se/qfmlvc.png http://a.pomf.se/mcamlr.png http://a.pomf.se/vhitxl.webm http://a.pomf.se/nyvwft.webm

3. `waves`: Fuzzy waves of approximately the same widths.
4. `none`: Sort entire rows.

* **`m`(multichannel mode):** Whether or not to sort each channel separately. Activate by passing `y` (`n` by default).
Examples: http://a.pomf.se/txvbmf.png http://a.pomf.se/sgwbum.png http://a.pomf.se/jsvcgy.png

* **`o`(output file):** Path of output file. Randomly generates a file name by default.

* **`r`(randomness):** What % of intervals *not* to sort. 0 by default.

* **`t`(threshold):** Defines the threshold while performing edge detection. `100` by default.

* **`c`(clength):** Characteristic length for the random width generator.

### todo

* Allow defining different intervals for different channels.
* Sorting along arbitrary functions

---

Based on https://gist.github.com/LycaonIsAWolf/667c5554e5d9d9a25ae6