"""
--- Day 14: Chocolate Charts ---

You finally have a chance to look at all of the produce moving around. Chocolate, cinnamon, mint, chili peppers, nutmeg, vanilla...
the Elves must be growing these plants to make hot chocolate! As you realize this, you hear a conversation in the distance.
When you go to investigate, you discover two Elves in what appears to be a makeshift underground kitchen/laboratory.

The Elves are trying to come up with the ultimate hot chocolate recipe; they're even maintaining a scoreboard which tracks the quality score (0-9) of each recipe.
Only two recipes are on the board: the first recipe got a score of 3, the second, 7.
Each of the two Elves has a current recipe: the first Elf starts with the first recipe, and the second Elf starts with the second recipe.
To create new recipes, the two Elves combine their current recipes. This creates new recipes from the digits of the sum of the current recipes' scores.
With the current recipes' scores of 3 and 7, their sum is 10, and so two new recipes would be created: the first with score 1 and the second with score 0.
If the current recipes' scores were 2 and 3, the sum, 5, would only create one recipe (with a score of 5) with its single digit.

The new recipes are added to the end of the scoreboard in the order they are created. So, after the first round, the scoreboard is 3, 7, 1, 0.
After all new recipes are added to the scoreboard, each Elf picks a new current recipe.
To do this, the Elf steps forward through the scoreboard a number of recipes equal to 1 plus the score of their current recipe.
So, after the first round, the first Elf moves forward 1 + 3 = 4 times, while the second Elf moves forward 1 + 7 = 8 times.
If they run out of recipes, they loop back around to the beginning.
After the first round, both Elves happen to loop around until they land on the same recipe that they had in the beginning; in general, they will move to different recipes.

Drawing the first Elf as parentheses and the second Elf as square brackets, they continue this process:

(3)[7]
(3)[7] 1  0
 3  7  1 [0](1) 0
 3  7  1  0 [1] 0 (1)
(3) 7  1  0  1  0 [1] 2
 3  7  1  0 (1) 0  1  2 [4]
 3  7  1 [0] 1  0 (1) 2  4  5
 3  7  1  0 [1] 0  1  2 (4) 5  1
 3 (7) 1  0  1  0 [1] 2  4  5  1  5
 3  7  1  0  1  0  1  2 [4](5) 1  5  8
 3 (7) 1  0  1  0  1  2  4  5  1  5  8 [9]
 3  7  1  0  1  0  1 [2] 4 (5) 1  5  8  9  1  6
 3  7  1  0  1  0  1  2  4  5 [1] 5  8  9  1 (6) 7
 3  7  1  0 (1) 0  1  2  4  5  1  5 [8] 9  1  6  7  7
 3  7 [1] 0  1  0 (1) 2  4  5  1  5  8  9  1  6  7  7  9
 3  7  1  0 [1] 0  1  2 (4) 5  1  5  8  9  1  6  7  7  9  2

The Elves think their skill will improve after making a few recipes (your puzzle input). However, that could take ages; you can speed this up considerably by identifying the scores of the ten recipes after that. For example:

    If the Elves think their skill will improve after making 9 recipes, the scores of the ten recipes after the first nine on the scoreboard would be 5158916779 (highlighted in the last line of the diagram).
    After 5 recipes, the scores of the next ten would be 0124515891.
    After 18 recipes, the scores of the next ten would be 9251071085.
    After 2018 recipes, the scores of the next ten would be 5941429882.

What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?

Your puzzle input is 293801.
"""

##class Node(object):
##    def __init__(self, value, p=None, n=None):
##        self.value = value
##        self.p = p
##        self.n = n
##
##    def get_next(self, idx):
##        if idx == 0:
##            return self
##        else:
##            return self.n.get_next(idx-1)
##
##    def get_previous(self, idx):
##        if idx == 0:
##            return self
##        else:
##            return self.p.get_previous(idx-1)
##
##    def set_next(self, n):
##        self.n = n
##
##    def set_previous(self, p):
##        self.p = p
##
##
##class ScoreBoard(object):
##    def __init__(self):
##        self.front = Node(3)
##        self.back = Node(7)
##        self.front.set_next(self.back)
##        self.back.set_previous(self.front)
##
##    def push_back(self, node):
##        node.set_previous(self.back)
##        self.back.set_next(node)
##        self.back = node


class ScoreBoard(object):
    def __init__(self):
        self.scores = [3,7]
        self.elfs = [0,1]

    def __len__(self):
        return len(self.scores)

    def generate(self):
        s = sum(self.scores[e] for e in self.elfs)
        digits = [int(d) for d in str(s)]
        self.scores.extend(digits)
        addelfs = [self.scores[e]+1 for e in self.elfs]
        self.elfs = [(e + a)%len(self.scores) for e,a in zip(self.elfs, addelfs)]

    def __repr__(self):
        res = []
        for idx, s in enumerate(self.scores):
            if idx == self.elfs[0]:
                res.append("({0})".format(s))
            elif idx == self.elfs[1]:
                res.append("[{0}]".format(s))
            else:
                res.append(" {0} ".format(s))
        return " ".join(res)


def _get_input():
    with open("inputs/day14.txt") as f:
        return f.read().strip()

def _generate_scores_for(N):
    board = ScoreBoard()
    #print board
    while len(board) < N:
        board.generate()
        #print board
    return board




def get_score_of_ten_next_recipes():
##    print "f(5)==0124515891?", "".join(str(v) for v in _generate_scores_for(5+10).scores[5:5+10]) == "0124515891"
##    print "f(18)==9251071085?", "".join(str(v) for v in _generate_scores_for(18+10).scores[18:18+10]) == "9251071085"
##    print "f(2018)==5941429882?", "".join(str(v) for v in _generate_scores_for(2018+10).scores[2018:2018+10]) == "5941429882"

    N = int(_get_input())
    return "".join(str(v) for v in _generate_scores_for(N+10).scores[N:N+10])

"""
--- Part Two ---

As it turns out, you got the Elves' plan backwards. They actually want to know how many recipes appear on the scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

    51589 first appears after 9 recipes.
    01245 first appears after 5 recipes.
    92510 first appears after 18 recipes.
    59414 first appears after 2018 recipes.

How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
"""

def _generate_scores_until_appears(sequence, maxiter=3000):
    N = len(sequence)
    board = ScoreBoard()

    for idx in range(maxiter):
        board.generate()
        last_scores = "".join(str(v) for v in board.scores[-(N+2):])
        if sequence in last_scores:
            scores = "".join(str(v) for v in board.scores)
            return scores.find(sequence)

    return None


def _print_board_sequences(N):
    board = ScoreBoard()
    print board
    for idx in range(N):
        board.generate()
        print idx, "::", board

def get_nb_recipes_to_get_sequence():
##    print "f(51589)==9?", _generate_scores_until_appears("51589") == 9
##    print "f(01245)==5?", _generate_scores_until_appears("01245") == 5
##    print "f(92510)==18?", _generate_scores_until_appears("92510") == 18
##    print "f(59414)==2018?", _generate_scores_until_appears("59414") == 2018

    sequence = _get_input()
    return _generate_scores_until_appears(sequence, 100000000)

def check():
    print("- Part 1: %s"% (get_score_of_ten_next_recipes()=="3147574107",)) #Your puzzle answer was 3147574107.
    print("- Part 2: %s"% (get_nb_recipes_to_get_sequence()==20280190,)) #Your puzzle answer was 20280190.


if __name__ == '__main__':
    print("Part 1: get score of ten next recipes: %s" % get_score_of_ten_next_recipes())
    print("Part 2: get nb recipes to get sequence: %s" % get_nb_recipes_to_get_sequence())
