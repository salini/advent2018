"""
--- Day 11: Chronal Charge ---

You watch the Elves and their sleigh fade into the distance as they head toward the North Pole. Actually, you're the one fading. The falling sensation returns.
The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a hologram of the situation: a 300x300 grid of fuel cells and their current power levels, some negative.
You're not sure what negative power means in the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction. In X,Y notation, the top-left cell is 1,1, and the top-right cell is 300,1.
The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your destination, you decide to choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the following process:

    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level.

For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:

    The rack ID is 3 + 10 = 13.
    The power level starts at 13 * 5 = 65.
    Adding the serial number produces 65 + 8 = 73.
    Multiplying by the rack ID produces 73 * 13 = 949.
    The hundreds digit of 949 is 9.
    Subtracting 5 produces 9 - 5 = 4.

So, the power level of this fuel cell is 4.

Here are some more example power levels:

    Fuel cell at  122,79, grid serial number 57: power level -5.
    Fuel cell at 217,196, grid serial number 39: power level  0.
    Fuel cell at 101,153, grid serial number 71: power level  4.

Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the 300x300 grid. Identify this square using the X,Y coordinate of its top-left fuel cell. For example:

For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these fuel cells appear in the middle of this 5x5 region:

-2  -4   4   4   4
-4   4   4   4  -5
 4   3   3   4  -4
 1   1   2   4  -3
-1   0   2  -5  -2

For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle of this region:

-3   4   2   2   2
-4   4   3   3   4
-5   3   3   4  -4
 4   3   3   4  -3
 3   3   3  -5  -1

What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?
"""

import numpy as np

from advent.log import show_log, log

from multiprocessing import Pool

#the top-left cell is 1,1, and the top-right cell is 300,1. #CAREFUL, it is transposed from numpy and starts from 1

def _compute_fuel_cells_power(grid, cdim=3):
    fuel_cells = np.zeros((grid.shape[0]-cdim+1, grid.shape[1]-cdim+1))

    for x in range(fuel_cells.shape[0]):
        for y in range(fuel_cells.shape[1]):
            fuel_cells[x,y] = np.sum(grid[x:x+cdim, y:y+cdim])

    return fuel_cells


def _find_largest_fuel_cells(grid, cdim=3):
    fuel_cells = _compute_fuel_cells_power(grid, cdim)
    maxfc_idx = fuel_cells.argmax()
    coord = np.unravel_index(maxfc_idx, fuel_cells.shape)
    maxpower = fuel_cells[coord]
    COORD = (coord[0]+1, coord[1]+1)
    return COORD, maxpower


def _get_levels(arguments):
    grid, cdim = arguments
    coord, maxpower = _find_largest_fuel_cells(grid, cdim)
    return (maxpower, coord[0], coord[1], cdim)


def _find_largest_fuel_cells_with_size(grid, max_size=300):
    pool = Pool(8)
    grids = [grid.copy()]*max_size
    cdims = range(1, max_size+1)
    levels = pool.map(_get_levels, zip(grids, cdims) )

    return max(levels, key=lambda x: x[0])[1:]


class PowerGrid(object):
    def __init__(self, serial_number, DIM=300):
        #init #here X is vertical, puzzle is horizontal
        Xcoord = np.dot(np.array(range(1,DIM+1)).reshape(-1,1), np.ones((1, DIM)) )
        Ycoord = np.dot(np.ones((DIM, 1)), np.array(range(1,DIM+1)).reshape(1,-1) )
        rackid = Xcoord + 10
        powerlevel = rackid * Ycoord
        powerlevel += serial_number
        powerlevel *= rackid

        hundreddigit = np.zeros((DIM,DIM), dtype=int)
        for x in range(DIM):
            for y in range(DIM):
                pl = powerlevel[x,y]
                hdigit = int(pl*0.01)
                hdigit = hdigit - (int(hdigit*0.1)*10)
                hundreddigit[x,y] = int(hdigit)

        self.grid = hundreddigit - 5
        self.block_power = None

    def get_power_level(self, X, Y):
        return self.grid[X-1, Y-1]

    def compute_fuel_cells_power(self, cdim=3):
        return _compute_fuel_cells_power(self.grid, cdim)

    def find_largest_fuel_cells(self, cdim=3):
        return _find_largest_fuel_cells(self.grid, cdim)

    def find_largest_fuel_cells_with_size(self, max_size=300):
        return _find_largest_fuel_cells_with_size(self.grid, max_size)

    def find_largest_fuel_cells_with_size_no_pool(self, max_size=300):
        levels =[]
        for cdim in range(1,max_size+1):
            print "compute %d" % cdim
            coord, maxpower = self.find_largest_fuel_cells(cdim)
            levels.append((maxpower, coord[0], coord[1], cdim))

        return max(levels, key=lambda x: x[0])[1:]


def _get_serial_number():
    with open("inputs/day11.txt") as f:
        return int(f.read())


def get_coordinate_of_top_left_fuel_cell():
##    print "is 4? %d" % PowerGrid(8, 10).get_power_level(3,5)
##    print "is -5? %d" % PowerGrid(57, 125).get_power_level(122,79)
##    print "is 0? %d" % PowerGrid(39, 220).get_power_level(217,196)
##    print "is 4? %d" % PowerGrid(71, 160).get_power_level(101,153)

##    print "is (33,45), 29? %s, %s" % PowerGrid(18).find_largest_fuel_cells()
##    print "is (21,61), 30 ? %s, %s" % PowerGrid(42).find_largest_fuel_cells()

    serial_number = _get_serial_number()
    return PowerGrid(serial_number).find_largest_fuel_cells()[0]

"""
--- Part Two ---

You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power.
Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

    For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
    For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.

What is the X,Y,size identifier of the square with the largest total power?
"""

def get_coordinate_of_top_left_fuel_cell_with_size():
##    print "is 90,269,16? %s" % (PowerGrid(18).find_largest_fuel_cells_with_size(),)
##    print "is 232,251,12? %s" % (PowerGrid(42).find_largest_fuel_cells_with_size(),)
    serial_number = _get_serial_number()
    return PowerGrid(serial_number).find_largest_fuel_cells_with_size()



def check():
    print("- Part 1: %s"% (get_coordinate_of_top_left_fuel_cell()==(21,68),))
    print("- Part 2: %s"% (get_coordinate_of_top_left_fuel_cell_with_size()==(90,201,15),))


if __name__ == '__main__':
    print("Part 1: get coordinate of top-left fuel cell: %s" % (get_coordinate_of_top_left_fuel_cell(),))
    print("Part 2: get coordinate of top-left fuel cell with size: %s" % (get_coordinate_of_top_left_fuel_cell_with_size(),))

