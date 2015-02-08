# pixelsort

## selectiveSort

Runs an edge detection to split each row into intervals, then sorts each interval by R+G+B.

Threshold for edge detection can ve set by the `threshold` parameter.

Examples: http://a.pomf.se/qfmlvc.png http://a.pomf.se/mcamlr.png http://a.pomf.se/vhitxl.webm http://a.pomf.se/nyvwft.webm

## randomSort

Splits rows into intervals of random widths, then sorts the intervals. The probability distribution of the widths can be specified, by default it's the Maxwell–Boltzmann distribution (for no particular reason).

Based on https://gist.github.com/LycaonIsAWolf/667c5554e5d9d9a25ae6