"""
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night).
Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit.
All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric.
Each claim's rectangle is defined as follows:

    The number of inches between the left edge of the fabric and the left edge of the rectangle.
    The number of inches between the top edge of the fabric and the top edge of the rectangle.
    The width of the rectangle in inches.
    The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall.
Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric.
How many square inches of fabric are within two or more claims?
"""

import numpy as np

class Slice(object):
    def __init__(self, cid, l, t, w, h):
        self.__dict__.update(dict(cid=cid, l=l, t=t, w=w, h=h))

def _get_all_slices(lines):
    slices = []
    for l in lines:
        cid, sep, data = l.partition("@")
        data = data.replace(":", " ").replace("x", " ").replace(",", " ")
        data = [int(d) for d in data.split()]
        slices.append(Slice(int(cid[1:]), *data))

    return slices

def _get_max_dim(slices):
    max_m_width = -1
    max_m_height = -1
    for s in slices:
        max_m_width = max(max_m_width, s.l + s.w)
        max_m_height = max(max_m_height, s.t + s.h)

    return max_m_width, max_m_height

def get_intersecting_surface():
    with open("inputs/day03.txt") as f:
        lines = f.readlines()

    slices = _get_all_slices(lines)
    fabric = np.zeros(_get_max_dim(slices))  # create a matrix with the max dimension of the fabric

    for s in slices: #concatenate all slices
        fabric[s.l:s.l+s.w, s.t:s.t+s.h] += 1

    #We count where there is more than 1
    intersection = np.sum(fabric>1)
    return intersection




"""
--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim.
If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?

"""

def get_non_intersecting_claim_ID():
    with open("inputs/day03.txt") as f:
        lines = f.readlines()

    slices = _get_all_slices(lines)

    dims = _get_max_dim(slices)
    fabric = np.zeros(dims)  # create a matrix with the max dimension of the fabric

    for s in slices: #concatenate all slices
        fabric[s.l:s.l+s.w, s.t:s.t+s.h] += 1

    #we will then check that they remain untouched
    for s in slices:
        if s.w*s.h == np.sum(fabric[s.l:s.l+s.w, s.t:s.t+s.h]): #the rectangle is untouched
            return s.cid

    return None


if __name__ == '__main__':
    print("Part 1: get intersecting surface: %d" % get_intersecting_surface())
    print("Part 1: get non intersecting claim ID: %s" % get_non_intersecting_claim_ID())
