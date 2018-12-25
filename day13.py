"""
--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on.
The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.
Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along.
They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.
Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+).
Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>).
(On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)
Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on.
This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time.
They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on.
Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square.
Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart.
The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/

After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash.
Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/

In this example, the location of the first crash is 7,3.
"""

from advent.log import show_log, log

import numpy as np

class Kart(object):
    symbols = ["^", "v", ">", "<", "X"]
    cyclic = [">", "^", "<", "v"]
    kartnum=0

    def __init__(self, row, col, state):
        self.name = 'kart{0}'.format(Kart.kartnum)
        Kart.kartnum += 1
        self.coord = np.array([row, col])
        self.state = state
        self.trajectory = []
        self.next_command = 0
        self.save_traj()

    def save_traj(self):
        self.trajectory.append( (self.state, self.coordinate()) )

    def set_collided(self):
        self.state = "X"
        self.trajectory.pop()
        self.save_traj()

    def coordinate(self):
        return tuple(self.coord)

    def integrate(self):
        if self.state == ">":
            self.coord[1] += 1
        elif self.state == "<":
            self.coord[1] += -1
        elif self.state == "v":
            self.coord[0] += 1
        elif self.state == "^":
            self.coord[0] += -1

    def turn_left(self):
        idx = Kart.cyclic.index(self.state)
        self.state = Kart.cyclic[(idx+1)%len(Kart.cyclic)]

    def turn_right(self):
        idx = Kart.cyclic.index(self.state)
        self.state = Kart.cyclic[(idx-1)%len(Kart.cyclic)]

    def move(self, track_state):
        if self.state == "X":
            return

        if track_state not in ["|", "-", "\\", "/","+"]:
            raise ValueError("track state is wrong: '"+track_state+"'")
        if track_state == "|":
            if self.state not in ["^", "v"]:
                raise ValueError("kart direction is wrong '%s' on '%s'" % (self.state, track_state))
        elif track_state == "-":
            if self.state not in [">", "<"]:
                raise ValueError("kart direction is wrong '%s' on '%s'" % (self.state, track_state))
        elif track_state == "\\":
            if self.state in [">", "<"]:
                self.turn_right()
            elif self.state in ["v", "^"]:
                self.turn_left()
            else:
                raise ValueError("kart direction is wrong '%s' on '%s'" % (self.state, track_state))
        elif track_state == "/":
            if self.state in [">", "<"]:
                self.turn_left()
            elif self.state in ["v", "^"]:
                self.turn_right()
            else:
                raise ValueError("kart direction is wrong '%s' on '%s'" % (self.state, track_state))
        elif track_state == "+":
            if self.next_command == 0:
                self.turn_left()
            if self.next_command == 2:
                self.turn_right()
            self.next_command = (self.next_command +1)%3

        self.integrate()
        self.save_traj()

    def __repr__(self):
        return "kart(%s:%s)" % (self.state, self.coordinate())


class Track(object):
    symbols = [" ", "|", "-", "\\", "/","+"]

    def __init__(self, track_raw):
        track_raw = [line for line in track_raw.split("\n") if len(line) > 0]
        Nrow = len(track_raw)
        Ncol = max(len(l) for l in track_raw)
        self.map = np.ones((Nrow, Ncol), dtype=int)*ord(" ")
        self.karts = []

        for row, line in enumerate(track_raw):
            for col, elem in enumerate(line):
                if elem in Track.symbols:
                    self.map[row, col] = ord(elem)
                elif elem in Kart.symbols:
                    self.karts.append(Kart(row, col, elem))
                    if elem in ["<", ">"]:
                        self.map[row, col] = ord("-")
                    else:
                        self.map[row, col] = ord("|")
                else:
                    raise ValueError("elem is not valid: '"+elem+"'")

    def __repr__(self):
        str_map = self.map.copy()
        for k in self.karts:
            str_map[k.coordinate()] = ord(k.state)
        return "\n".join("".join(chr(v) for v in line) for line in str_map)


    def do_tick(self, return_when_crash=False):
        def get_kart_order(k0, k1):
            if k0.coord[0] < k1.coord[0]:
                return -1
            elif k0.coord[0] > k1.coord[0]:
                return 1
            else:
                if k0.coord[1] < k1.coord[1]:
                    return -1
                elif k0.coord[1] > k1.coord[1]:
                    return 1
                else:
                    return 0

        ordered_kart = sorted(self.karts, cmp=get_kart_order)

        for k in ordered_kart:
            k.move(chr(self.map[k.coordinate()]))

            for kother in ordered_kart:
                if k is not kother and k.state!="X" and kother.state!="X" and all(k.coord == kother.coord):
                    k.set_collided()
                    kother.set_collided()
                    if return_when_crash:
                        return k.coordinate()

        return False

    def clean_crashed_karts(self):
        N = len(self.karts)
        crashed_kart = [k for k in self.karts if k.state == "X"]
        self.karts = [k for k in self.karts if k.state != "X"]
        if len(crashed_kart):
            return crashed_kart
        else:
            False


def _load_track_example():
    track_raw = r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
"""
    return Track(track_raw)


def _load_track():
    with open("inputs/day13.txt") as f:
        return Track(f.read())


def get_first_collision_coordinate():
    #track = _load_track_example()
    track = _load_track()
    log(track)

    N = 10000
    for i in range(N):
        log("================ %d" %i)
        res = track.do_tick(return_when_crash=True)
        if res != False:
            log(track)
            return (res[1], res[0]) #inverted
            break

    log("no collision detected in this amount of ticks (%d)" % N)
    return None



"""
--- Part Two ---

There isn't much you can do to prevent crashes in this ridiculous system.
However, by predicting the crashes, the Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.
They can proceed like this for a while, but eventually, they're going to run out of carts.
It could be useful to figure out where the last cart that hasn't crashed will end up.

For example:

/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\
|   |
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\
|   |
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\
|   |
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/

After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.
What is the location of the last cart at the end of the first tick where it is the only cart left?
"""

def _load_track_example2():
    track_raw = r"""
/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""
    return Track(track_raw)


def get_last_kart_coordinate():
    #track = _load_track_example2()
    track = _load_track()

    N = 100000
    for idx in range(N):

        res = track.do_tick()

        collisions = track.clean_crashed_karts()
##        if collisions:
##            log("================ %d" %idx)
##            log("Collision(s) occured")
##            for c in collisions:
##                log("--- %s" % (c.coordinate(),))
##            log("%d karts remaining" % len(track.karts))

        if len(track.karts) == 1:
            log("================ %d" %idx)
            c = track.karts[0].coordinate()
            return (c[1], c[0]) #inverted

        elif len(track.karts) == 0:
            log("no more karts!")
            return None

    return None

def check():
    print("- Part 1: %s"% (get_first_collision_coordinate()==(116, 10),)) #Your puzzle answer was 116,10.
    print("- Part 2: %s"% (get_last_kart_coordinate()==(116, 25),)) #Your puzzle answer was 116,25.


if __name__ == '__main__':
    check()
    show_log(True)
    print("Part 1: get first collision coordinate: %s" % (get_first_collision_coordinate(),))
    print("Part 2: get last kart coordinate: %s" % (get_last_kart_coordinate(),))

