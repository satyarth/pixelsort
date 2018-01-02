# pixelsort

### What is Pixel Sorting?

Have a look at [this post](http://satyarth.me/articles/pixel-sorting/) or [/r/pixelsorting](http://www.reddit.com/r/pixelsorting/top/)

### Dependencies

Tested with python3. Should work with python2 as well.

Requires Pillow. `pip install Pillow` should work. If not, see [here](https://pillow.readthedocs.org/en/3.0.0/installation.html#linux-installation) for details.

There is also a requirements file which pretty much does the same via `pip install -r requirements.txt`.

### Usage

From the command line:

```
git clone https://github.com/satyarth/pixelsort.git
cd pixelsort
python3 pixelsort.py %PathToImage% [options]
```

Tip: To replicate Kim Asendorf's original [processing script](https://github.com/kimasendorf/ASDFPixelSort), first sort vertically and then horizontally in `threshold` (default) mode:

```
python3 pixelsort.py %PathToImage% -a 90
python3 pixelsort.py %PathToSortedImage%
```

#### Parameters:

Parameter 			| Flag 	| Description
--------------------|-------|------------
Interval function 	| `-i`	| Controls how the intervals used for sorting are defined. See below for more details and examples.
Output file 		| `-o`	| Path of output file. Randomly generates a file name by default.
Randomness 			| `-r`	| What percentage of intervals *not* to sort. 0 by default.
Threshold (lower) 	| `-t`	| How dark must a pixel be to be considered as a 'border' for sorting? Takes values from 0-1. 0.25 by default. Used in `edges` and `threshold` modes.
Threshold (upper) 	| `-u`	| How bright must a pixel be to be considered as a 'border' for sorting? Takes values from 0-1. 0.8 by default. Used in `threshold` mode.
Char. length		| `-c`	| Characteristic length for the random width generator. Used in mode `random`.
Angle 				| `-a`	| Angle at which you're pixel sorting in degrees. `0` (horizontal) by default.
External int file 	| `-f` 	| Image used to define intervals. Must be black and white.
Sorting function    | `-s`  | Sorting function to use for sorting the pixels.

#### Interval Functions

Interval function 	| Description
--------------------|------------
`random`			| Randomly generate intervals. Distribution of widths is linear by default. Interval widths can be scaled using `clength`.
`edges`				| Performs an edge detection, which is used to define intervals. Tweak threshold with `threshold`.
`threshold`			| Intervals defined by lightness thresholds; only pixels with a lightness between the upper and lower thresholds are sorted.
`waves`				| Intervals are waves of nearly uniform widths. Control width of waves with `clength`.
`file`				| Intervals taken from another specified input image. Must be black and white.
`none`				| Sort whole rows, only stopping at image borders.


#### Sorting Functions

Sorting function    | Description
--------------------|------------
`lightness`         | Sort by the lightness of a pixel according to a HSV representation.
`hue`               | Sort by the hue of a pixel according to a HSV representation.
`saturation`        | Sort by the saturation of a pixel according to a HSV representation.
`intensity`         | Sort by the intensity of a pixel, i.e. the sum of all the RGB values.
`minimum`           | Sort on the minimum RGB value of a pixel (either the R, G or B).

#### Examples

`python3 pixelsort.py examples/image.jpg -i random -c 20`

![random](/examples/random.png)

`python3 pixelsort.py examples/image.jpg -i edges -t 250`

![edges](/examples/edges.png)

* `file`: Intervals taken from image specified with `-f`. Must be black and white.

`python3 pixelsort.py examples/image.jpg -i file -f examples/intervals.png `

![file](/examples/intervals.png)

(generated with [elementary-ca](https://github.com/satyarth/elementary-ca))

![file](/examples/file.png)

### todo

* Allow defining different intervals for different channels.

---

Based on https://gist.github.com/LycaonIsAWolf/667c5554e5d9d9a25ae6
