# pixelsort

### What is Pixel Sorting?

Have a look at [this post](http://satyarth.me/articles/pixel-sorting/) or [/r/pixelsorting](http://www.reddit.com/r/pixelsorting/top/)

### Dependencies

Should work in both Python 2 and 3, but Python 3 is recommended.

## Usage

From the command line:

```
pip install pixelsort
python3 -m pixelsort %PathToImage% [options]
```

Tip: To replicate Kim Asendorf's original [processing script](https://github.com/kimasendorf/ASDFPixelSort), first sort vertically and then horizontally in `threshold` (default) mode:

```
python3 -m pixelsort %PathToImage% -a 90
python3 -m pixelsort %PathToSortedImage%
```

As a package:

```
>>> from pixelsort import pixelsort
>>> from PIL import Image
>>> a = Image.open("examples/image.jpg")
>>> a
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=576x324 at 0x7F8F6A2AC208>
>>> pixelsort(a)
<PIL.Image.Image image mode=RGBA size=576x324 at 0x7F8F66AA57B8>
```

#### Parameters:

Parameter 			        | Flag 	| Description
------------------------|-------|------------
Interval function     	| `-i`	| Controls how the intervals used for sorting are defined. See below for more details and examples. Threshold by default.
Output path             | `-o`	| Path of output file. Uses the current time for the file name by default.
Randomness 			        | `-r`	| What percentage of intervals *not* to sort. 0 by default.
Threshold (lower)     	| `-t`	| How dark must a pixel be to be considered as a 'border' for sorting? Takes values from 0-1. 0.25 by default. Used in `edges` and `threshold` modes.
Threshold (upper)     	| `-u`	| How bright must a pixel be to be considered as a 'border' for sorting? Takes values from 0-1. 0.8 by default. Used in `threshold` mode.
Char. length		        | `-c`	| Characteristic length for the random width generator. Used in mode `random` and `waves`.
Angle 				          | `-a`	| Angle at which you're pixel sorting in degrees. `0` (horizontal) by default.
External interval file 	| `-f` 	| Image used to define intervals. Must be black and white.
Sorting function        | `-s`  | Sorting function to use for sorting the pixels. Lightness by default.
Mask                    | `-m`  | Image used for masking parts of the image.
Logging level           | `-l`  | Level of logging statements made visible. Choices include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. `WARNING` by default.

#### Interval Functions

Interval function | Description
------------------|------------
`random`			    | Randomly generate intervals. Distribution of widths is linear by default. Interval widths can be scaled using `char_length`.
`edges`				    | Performs an edge detection, which is used to define intervals. Tweak threshold with `threshold`.
`threshold`		  	| Intervals defined by lightness thresholds; only pixels with a lightness between the upper and lower thresholds are sorted.
`waves`			    	| Intervals are waves of nearly uniform widths. Control width of waves with `char_length`.
`file`			    	| Intervals taken from another specified input image. Must be black and white, and the same size as the input image.
`file-edges`	  	| Intevals defined by performing edge detection on the file specified by `-f`. Must be the same size as the input image.
`none`			    	| Sort whole rows, only stopping at image borders.


#### Sorting Functions

Sorting function  | Description
------------------|------------
`lightness`       | Sort by the lightness of a pixel according to a HSL representation.
`hue`             | Sort by the hue of a pixel according to a HSL representation.
`saturation`      | Sort by the saturation of a pixel according to a HSL representation.
`intensity`       | Sort by the intensity of a pixel, i.e. the sum of all the RGB values.
`minimum`         | Sort on the minimum RGB value of a pixel (either the R, G or B).

#### Examples

`python3 -m pixelsort examples/image.jpg -i random -c 20`

![random](/examples/random.png)

`python3 -m pixelsort examples/image.jpg -i edges -t .5`

![edges](/examples/edges.png)

* `file`: Intervals taken from image specified with `-f`. Must be black and white.

`python3 -m pixelsort examples/image.jpg -i file -f examples/intervals.png `

![file](/examples/intervals.png)

(generated with [elementary-ca](https://github.com/satyarth/elementary-ca))

![file](/examples/file.png)

* `mask`: Mask taken from image specified with `-m`. Must be black and white.

`python3 -m pixelsort examples/image.jpg -i random -c 20 -m examples/mask.png`

![file](/examples/mask.png)

![file](/examples/masked.png)

### Todo

* Allow defining different intervals for different channels.

---

Based on https://gist.github.com/prophetgoddess/667c5554e5d9d9a25ae6
