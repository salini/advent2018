"""
--- Day 5: Alchemical Reduction ---

You've managed to sneak in to the prototype suit manufacturing lab.
The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better.
You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed.
Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

    In aA, a and A react, leaving nothing behind.
    In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
    In abAB, no two adjacent units are of the same type, and so nothing happens.
    In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.

Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.

After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others, the input is large; if you copy/paste your input, make sure you get the whole thing.)

"""

import numpy as np


def _load_full_polymer():
    with open("inputs/day05.txt") as f:
        polymer = f.read()
    return polymer.strip()


def _is_reacting(c0,c1):
    """ the polarity between 'a' and 'A' is a difference of 32 between ascii number
    """
    return True if abs(ord(c0)-ord(c1))==32 else False


def _reduce_polymer(polymer):
    Lpoly = polymer
    while True:
        N = len(Lpoly)
        mask = np.ones(N)
        #print N
        for idx, el in enumerate(Lpoly[0:-1]):
            if all(mask[idx:idx+2]) and _is_reacting(Lpoly[idx], Lpoly[idx+1]):
                mask[idx:idx+2] = 0

        Lpoly = [e for idx, e in enumerate(Lpoly) if mask[idx]]

        if N != len(Lpoly):
            continue
        else:
            break

    #print Lpoly
    return Lpoly


def get_polymer_units():
    polymer = _load_full_polymer()
    reduced_polymer = _reduce_polymer(polymer)
    return len(reduced_polymer)




"""
--- Part Two ---

Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should.
Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

    Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
    Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
    Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
    Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.

In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""

from multiprocessing import Pool

def _polymer_opti(elem):
    polymer = _load_full_polymer()
    polymer = polymer.replace(elem, "").replace(elem.upper(), "") #remove element in polymer
    reduced_polymer = _reduce_polymer(polymer)
    return len(reduced_polymer)


def get_optimize_polymer_units():
    pool = Pool(8)
    elements = "abcdefghijklmnopqrstuvwxyz"
    res = pool.map(_polymer_opti, list(elements))
    poly_res = dict(zip(elements, res))
    print poly_res
    print "==================="
    best_poly = min(poly_res.items(), key=lambda x: x[1])
    print best_poly
    return best_poly[1]


if __name__ == '__main__':
    print("Part 1: get polymer units: %s" % get_polymer_units())
    print("Part 2: get optimized polymer units: %s" % get_optimize_polymer_units())
