
"""
--- Day 12: Subterranean Sustainability ---

The year 518 is significantly more underground than your history books implied. Either that, or you've arrived in a vast cavern network under the North Pole.
After exploring a little, you discover a long tunnel that contains a row of small pots as far as you can see to your left and right.
A few of them contain plants - someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3....
Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.)
For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: someone has been trying to figure out how these plants spread to nearby pots.
Based on the notes, for each generation of plants, a given pot has or does not have a plant based on whether that pot (and the two pots on either side of it) had a plant in the last generation.
These are written as LLCRR => N, where L are pots to the left, C is the current pot being considered, R are the pots to the right, and N is whether the current pot will have a plant in the next generation. For example:

    A note like ..#.. => . means that a pot that contains a plant but with no plants within two pots of it will not have a plant in it during the next generation.
    A note like ##.## => . means that an empty pot with two plants on each side of it will remain empty in the next generation.
    A note like .##.# => # means that a pot has a plant in a given generation if, in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.

It's not clear what these plants are for, but you're sure it's important, so you'd like to make sure the current configuration of plants is sustainable by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #

For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3
       0         0         0         0
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.

The generation is shown along the left, where 0 is the initial state. The pot numbers are shown along the top, where 0 labels the center pot, negative-numbered pots extend to the left, and positive pots extend toward the right.
Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.
After one generation, only seven plants remain. The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#., pot 9 matched .##.., and so on.
In this example, after 20 generations, the pots shown as # contain plants, the furthest left of which is pot -2, and the furthest right of which is pot 34.
Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?
"""

from advent.log import show_log, log

import numpy as np

def _convert(state):
    return np.array([False if v=="." else True for v in state])


class Rule(object):
    def __init__(self, condition, result):
        self.condition = condition
        self.result = result

    def is_verified(self, table):
        if all(table == self.condition):
            return True
        else:
            False

    def __repr__(self):
        return "%s => %s" % (self.condition, self.result)


class Pots(object):
    def __init__(self, state0, side_extensions=5):
        self.dim = side_extensions
        self.offset = self.dim
        self.state = np.array([False]*(len(state0) + 2*side_extensions))
        self.state[self.offset:self.offset+len(state0)] = state0
        self.buffer = self.state.copy()

    def get_state_str(self, has_plant="|", no_plant="."):
        return "".join(has_plant if s == True else no_plant for s in self.state)

    def apply_rules(self, rules):
        for x in range(2, len(self.state)-2):
            for r in rules:
                if r.is_verified(self.state[x-2:x+3]):
                    self.buffer[x] = r.result
                    break

        self.state[:] = self.buffer[:]

    def reshape_if_needed(self):
        if all(self.state[:self.dim] == False):
            self.state = self.state[self.dim:]
            self.offset -= self.dim
            self.buffer = self.state.copy()

        if any(self.state[:5] == True):
            self.state = np.hstack(([False]*self.dim, self.state))
            self.offset += self.dim
            self.buffer = self.state.copy()

        if any(self.state[-5:] == True):
            self.state = np.hstack((self.state, [False]*self.dim))
            self.buffer = self.state.copy()


    def get_sum(self):
        plants = np.array([idx for idx, v in enumerate(self.state) if v == True]) - self.offset
        return sum(plants)


def _get_state_and_rules():
    with open("inputs/day12.txt") as f:
        init_state = f.readline().replace("initial state:", "").strip()
        init_state = _convert(init_state)

        rules = []
        for l in f.readlines():
            if len(l.strip()):
                cond, sep, res = l.partition("=>")
                cond = cond.strip()
                res = _convert(res.strip())[0]
                rules.append(Rule(_convert(cond), res))

    return init_state, rules


def get_sum_of_pots():
    state0, rules = _get_state_and_rules()
    pots = Pots(state0, 10)
    log(pots.get_state_str())

    for i in range(20):
        pots.apply_rules(rules)
        pots.reshape_if_needed()
        log(pots.get_state_str())

    return pots.get_sum()

"""
--- Part Two ---

You realize that 20 generations aren't enough.
After all, these plants will need to last another 1500 years to even reach your timeline, not to mention your future.
After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
"""

import time


def _detect_stable_pattern(s0, s1):
    plant_left_0 = np.argmax(s0)
    plant_left_1 = np.argmax(s1)
    N = min( len(s0) - plant_left_0, len(s1) - plant_left_1)

    if all(s0[plant_left_0:plant_left_0+N] == s1[plant_left_1:plant_left_1+N]):
        return True, plant_left_1-plant_left_0
    return False

def get_sum_of_pots_huge():
    state0, rules = _get_state_and_rules()
    pots = Pots(state0, 10)

    # to optimize order of rules used?
    rules = sorted(rules, cmp=lambda x,y: list(x.condition).count(True)-list(y.condition).count(True))

    N = 50000000000
    idx = 0
    T = time.time()
    while idx < N:
        idx += 1

        prev_state = pots.state.copy()
        previous_sum = pots.get_sum()

        pots.apply_rules(rules)

        new_state =  pots.state.copy()
        new_sum = pots.get_sum()

        log(pots.get_state_str())
        pots.reshape_if_needed()

        result = _detect_stable_pattern(prev_state, new_state)
        if result != False:
            log("stable pattern DETECTED at iteration %d" %idx)
            current_sum = new_sum
            diff = new_sum - previous_sum

            total_sum = current_sum + diff * (N - idx)
            break

    return total_sum

def check():
    print("- Part 1: %s" % (get_sum_of_pots()==3051)) #Your puzzle answer was 3051.
    print("- Part 2: %s" % (get_sum_of_pots_huge()==1300000000669)) #Your puzzle answer was 1300000000669.


if __name__ == '__main__':
    show_log(True)
    print("Part 1: get sum of pots: %s" % get_sum_of_pots())
    print("Part 2: get sum of pots huge: %s" % get_sum_of_pots_huge())
