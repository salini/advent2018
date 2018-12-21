"""
--- Day 10: The Stars Align ---

It's no use; your navigation system simply isn't capable of providing walking directions in the arctic circle, and certainly not in 1018.

The Elves suggest an alternative. In times like these, North Pole rescue operations will arrange points of light in the sky to guide missing Elves back to base. Unfortunately, the message is easy to miss: the points move slowly enough that it takes hours to align them, but have so much momentum that they only stay aligned for a second. If you blink at the wrong time, it might be hours before another message appears.

You can see these points of light floating in the distance, and record their position in the sky and their velocity, the relative change in position per second (your puzzle input). The coordinates are all given from your perspective; given enough time, those positions and velocities will move the points into a cohesive message!

Rather than wait, you decide to fast-forward the process and calculate what the points will eventually spell.

For example, suppose you note the following points:

position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>

Each line represents one point. Positions are given as <X, Y> pairs: X represents how far left (negative) or right (positive) the point appears, while Y represents how far up (negative) or down (positive) the point appears.
At 0 seconds, each point has the position given. Each second, each point's velocity is added to its position. So, a point with velocity <1, -2> is moving to the right, but is moving upward twice as quickly. If this point's initial position were <3, 9>, after 3 seconds, its position would become <6, 3>.

Over time, the points listed above would move like this:

Initially:
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........

After 1 second:
......................
......................
..........#....#......
........#.....#.......
..#.........#......#..
......................
......#...............
....##.........#......
......#.#.............
.....##.##..#.........
........#.#...........
........#...#.....#...
..#...........#.......
....#.....#.#.........
......................
......................

After 2 seconds:
......................
......................
......................
..............#.......
....#..#...####..#....
......................
........#....#........
......#.#.............
.......#...#..........
.......#..#..#.#......
....#....#.#..........
.....#...#...##.#.....
........#.............
......................
......................
......................

After 3 seconds:
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................

After 4 seconds:
......................
......................
......................
............#.........
........##...#.#......
......#.....#..#......
.....#..##.##.#.......
.......##.#....#......
...........#....#.....
..............#.......
....#......#...#......
.....#.....##.........
...............#......
...............#......
......................
......................

After 3 seconds, the message appeared briefly: HI.
Of course, your message will be much longer and will take many more seconds to appear.

What message will eventually appear in the sky?
"""

import numpy as np
import pylab as pl

from advent.log import show_log, log

def _manhattan_distance(p0, p1):
    return abs(p0[0]-p1[0]) + abs(p0[1]-p1[1])


class Star(object):
    def __init__(self, pos, vel):
        self.pos = np.array(pos)
        self.vel = np.array(vel)

    def integrate(self):
        self.pos += self.vel

    def __repr__(self):
        return "p=%s, v=%s" % (self.pos, self.vel)


def are_connected(si_pos, sj_pos):
    if _manhattan_distance(si_pos, sj_pos) <= 2:
        return True
    else:
        False

def _get_stars():
    stars = []
    with open("inputs/day10.txt") as f:
        for l in f.readlines():
            #example: position=<-10466, -10485> velocity=< 1,  1>
            p, sep, v = l.partition("velocity=<")
            p = p.replace("position=<", "").replace(">", "")
            v = v.replace(">", "")
            pos = [int(d) for d in p.split(",")]
            vel = [int(d) for d in v.split(",")]
            stars.append(Star(pos, vel))
    return stars



def _get_adjacency_matrix(stars):
    N = len(stars)
    adj_mat = np.zeros((N,N))
    for idxi in range(N):
        for idxj in range(N):
            if idxi != idxj and are_connected(stars[idxi], stars[idxj]):
                adj_mat[idxi, idxj] = 1

    return adj_mat


def _get_subgraphs(stars_pos):
    adj_mat = _get_adjacency_matrix(stars_pos)

    def get_recursive_graph(cidx, remaining_nodes):
        connections = [n for n in remaining_nodes if adj_mat[cidx, n]==1]
        for n in connections:
            remaining_nodes.remove(n)
        subconnect = []
        for n in connections:
            subconnect.extend(get_recursive_graph(n, remaining_nodes))

        subconnect.append(cidx)
        return subconnect

    sub_graph_idx = []
    remaining_nodes = range(len(stars_pos))
    while len(remaining_nodes):
        cidx = remaining_nodes.pop(0)
        sub_graph = get_recursive_graph(cidx, remaining_nodes)
        sub_graph_idx.append(sub_graph)

    subgraphs = []
    for sgi in sub_graph_idx:
        subgraphs.append( np.array([stars_pos[idx] for idx in sgi]))

    return subgraphs


def _get_stars_systems_dim(stars_poses):
    return stars_poses.max(axis=1) - stars_poses.min(axis=1)


def get_message_in_sky(max_time=100000):
    stars = _get_stars()

    N = len(stars)

    stars_pos0 = np.array([s.pos for s in stars])   # init position
    stars_vel0 = np.array([s.vel for s in stars])   # init velocity
    log( "compute integrated positions...")
    stars_poses = np.array([stars_pos0 + stars_vel0*t for t in range(max_time)])

    log("compute system dimensions...")
    stars_sys_dim = _get_stars_systems_dim(stars_poses)

    log("filter possible systems (with small dimensions)...")
    possible_systems = [sp for sp,dim in zip(stars_poses, stars_sys_dim) if all(dim < 2*N)]
    log("%d possibility" % len(possible_systems))

    log("compute connexity...")
    connexity = [(len(_get_subgraphs(sp)),sp) for sp in possible_systems]
    min_connex_size, min_connex = min(connexity, key=lambda x: x[0])
    log("found with min connexity %d" % min_connex_size)

    subgraphs = _get_subgraphs(min_connex)

    pl.figure()
    for i,sg in enumerate(subgraphs):
        pl.plot(sg[:,0], -sg[:,1], "o", color = [float(i)/len(subgraphs)]*3)
        pl.grid()
        pl.axis('equal')
    pl.show()



"""
--- Part Two ---

Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds in the example above.

Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have needed to wait for that message to appear?
"""


def get_time_to_get_message(max_time=100000):
    stars = _get_stars()

    N = len(stars)

    stars_pos0 = np.array([s.pos for s in stars])   # init position
    stars_vel0 = np.array([s.vel for s in stars])   # init velocity
    log("compute integrated positions...")
    stars_poses = np.array([stars_pos0 + stars_vel0*t for t in range(max_time)])

    log("compute system dimensions...")
    stars_sys_dim = _get_stars_systems_dim(stars_poses)

    log("filter possible systems (with small dimensions)...")
    possible_systems = [(t, sp) for t, sp in enumerate(stars_poses) if all(stars_sys_dim[t] < 2*N)]
    log("%d possibility" % len(possible_systems))

    log("compute connexity...")
    connexity = [(t, len(_get_subgraphs(sp)),sp) for t, sp in possible_systems]
    T, min_connex_size, min_connex = min(connexity, key=lambda x: x[1])
    log("found at time %d with min connexity %d" % (T, min_connex_size))
    return T


def check():
    print("- Part 1: you need to run program and read by yourself") #Your puzzle answer was GEJKHGHZ.
    print("- Part 2: {0}".format(get_time_to_get_message()==10681)) #Your puzzle answer was 10681.

if __name__ == '__main__':
    show_log(True)
    print("Part 1: get message in sky: %s" % get_message_in_sky()) #reply "GEJKHGHZ"
    print("Part 2: get time to get message: %s" % get_time_to_get_message())

