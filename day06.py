
"""
--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling.
"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input).
Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.
If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).
Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.
In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid.
However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself).
Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""

import numpy as np
import pylab as pl

def _load_coordinates():
    with open("inputs/day06.txt") as f:
        coord = []
        for l in f.readlines():
            if l:
                a,b,c = l.partition(",")
                coord.append( (int(a), int(c)) )
        return coord

def _get_min_dimensions(coord):
    return [min(coord, key=lambda x: x[idx])[idx] for idx in [0,1]]

def _get_max_dimensions(coord):
    return [max(coord, key=lambda x: x[idx])[idx] for idx in [0,1]]

def _offset_coords(coord, offx, offy):
    return [(x+offx, y+offy) for x,y in coord]

def _manhattan_distance(p0, p1):
    return abs(p0[0]-p1[0]) + abs(p0[1]-p1[1])

def _get_distmap(coord):
    ## get matrix dimension
    maxx, maxy = _get_max_dimensions(coord)

    ## create mapping
    distmap = np.zeros((maxx,maxy, len(coord)))
    for x in range(distmap.shape[0]):
        for y in range(distmap.shape[1]):
            for d in range(distmap.shape[2]):
                distmap[x,y,d] = _manhattan_distance(coord[d], (x,y))

    return distmap


def get_largest_area():
    coord = _load_coordinates()

    ## get coordinate in minimum rectangle
    minx, miny = _get_min_dimensions(coord)
    coord = _offset_coords(coord, -minx, -miny)

    distmap = _get_distmap(coord)

    colormap = -1*np.ones(distmap.shape[0:2])
    for x in range(distmap.shape[0]):
        for y in range(distmap.shape[1]):
            m = min(distmap[x,y])
            w = np.where(distmap[x,y] == m)
            if len(w[0]) == 1:
                colormap[x,y] = w[0][0]

    ## if color touch a border, it is infinite, reset to -1
    color_reset = [-1]
    def _reset_border_color(c):
        if c not in color_reset:
            color_reset.append(c)
            colormap[np.where(colormap == c)] = -1

    for x in range(colormap.shape[0]):
        _reset_border_color(colormap[x,0])
        _reset_border_color(colormap[x,-1])

    for y in range(colormap.shape[1]):
        _reset_border_color(colormap[0,y])
        _reset_border_color(colormap[-1,y])

    ## if you whant to draw colormap...
##    pl.imshow(colormap)
##    coord = np.array(coord).T
##    pl.plot(coord[1], coord[0], "r.")
##    pl.show()

    unique, counts = np.unique(colormap, return_counts=True)
    area_size = dict(zip(unique, counts))
    del area_size[-1] #that is infinite areas

    maxarea = max(area_size.items(), key=lambda x: x[1])[1]
    return maxarea


"""
--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.
For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32.
For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region.
Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

In particular, consider the highlighted location 4,3 located at the top middle of the region.
Its calculation is as follows, where abs() is the absolute value function:

    Distance to coordinate A: abs(4-1) + abs(3-1) =  5
    Distance to coordinate B: abs(4-1) + abs(3-6) =  6
    Distance to coordinate C: abs(4-8) + abs(3-3) =  4
    Distance to coordinate D: abs(4-3) + abs(3-4) =  2
    Distance to coordinate E: abs(4-5) + abs(3-5) =  3
    Distance to coordinate F: abs(4-8) + abs(3-9) = 10
    Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

Because the total distance to all coordinates (30) is less than 32, the location is within the region.
This region, which also includes coordinates D and E, has a total size of 16.
Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.
What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""


def get_area_with_sum_distance_less_than(min_sum_dist=10000):
    coord = _load_coordinates()

    ## get coordinate in minimum rectangle
    minx, miny = _get_min_dimensions(coord)
    coord = _offset_coords(coord, -minx, -miny)

    distmap = _get_distmap(coord)

    summap = np.zeros(distmap.shape[0:2])
    for x in range(distmap.shape[0]):
        for y in range(distmap.shape[1]):
            summap[x,y] = sum(distmap[x,y])

    w_sum_dist = np.where(summap < min_sum_dist)
    return len(w_sum_dist[0])


def check():
    print("- Part 1: {0}".format(get_largest_area()==4171)) #Your puzzle answer was 4171.
    print("- Part 2: {0}".format(get_area_with_sum_distance_less_than()==39545)) #Your puzzle answer was 39545.

if __name__ == '__main__':
    print("Part 1: get largest area: %d" % get_largest_area())
    print("Part 1: get largest area: %d" % get_area_with_sum_distance_less_than())

