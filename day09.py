"""
--- Day 9: Marble Mania ---

You talk to the Elves while you wait for your navigation system to initialize. To pass the time, they introduce you to their favorite marble game.
The Elves play this game by taking turns arranging the marbles in a circle according to very particular rules.
The marbles are numbered starting with 0 and increasing by 1 until every marble has a number.

First, the marble numbered 0 is placed in the circle. At this point, while it contains only a single marble, it is still a circle: the marble is both clockwise from itself and counter-clockwise from itself.
This marble is designated the current marble.

Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble.
(When the circle is large enough, this means that there is one marble between the marble that was just placed and the current marble.) The marble that was just placed then becomes the current marble.

However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens.
First, the current player keeps the marble they would have placed, adding it to their score.
In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score.
The marble located immediately clockwise of the marble that was removed becomes the new current marble.

For example, suppose there are 9 players. After the marble with value 0 is placed in the middle, each player (shown in square brackets) takes a turn.
The result of each of those turns would produce circles of marbles like this, where clockwise is to the right and the resulting current marble is in parentheses:

[-] (0)
[1]  0 (1)
[2]  0 (2) 1
[3]  0  2  1 (3)
[4]  0 (4) 2  1  3
[5]  0  4  2 (5) 1  3
[6]  0  4  2  5  1 (6) 3
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7
[9]  0  8  4 (9) 2  5  1  6  3  7
[1]  0  8  4  9  2(10) 5  1  6  3  7
[2]  0  8  4  9  2 10  5(11) 1  6  3  7
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7
[4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7
[5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7
[6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
[7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15
[8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15
[9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15
[1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15
[2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15
[3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15
[4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15
[5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15
[6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15
[7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15

The goal is to be the player with the highest score after the last marble is used up.
Assuming the example above ends after the marble numbered 25, the winning score is 23+9=32 (because player 5 kept marble 23 and removed marble 9, while no other player got any points in this very short example game).

Here are a few more examples:

    10 players; last marble is worth 1618 points: high score is 8317
    13 players; last marble is worth 7999 points: high score is 146373
    17 players; last marble is worth 1104 points: high score is 2764
    21 players; last marble is worth 6111 points: high score is 54718
    30 players; last marble is worth 5807 points: high score is 37305

What is the winning Elf's score?
"""


class Game(object):
    def __init__(self, nb_players, last_marble):
        self.Nplayer = nb_players
        self.players = [0]*nb_players
        self.last_marble = last_marble

        self.circle = []

    def run(self):
        self.circle.append(0)

        cidx = 1 #current index
        for cm in range(1, self.last_marble + 1): #cm = current marble
            cp = (cm-1) % self.Nplayer
            if cm % 23 == 0:
                cidx = (cidx-7)%len(self.circle)
                self.players[cp] += cm + self.circle.pop(cidx)
            else:
                cidx = (cidx + 2)%len(self.circle)
                self.circle.insert(cidx, cm)

            #print self.get_state(cp, cidx)


    def run_fast(self):
        self.circle.append(0)

        cidx = 1 #current index
        for cm in range(1, self.last_marble + 1): #cm = current marble

            cp = (cm-1) % self.Nplayer
            if cm % 23 == 0:
                cidx = (cidx-7)%len(self.circle)
                self.players[cp] += cm + self.circle.pop(cidx)
            else:
                cidx = (cidx + 2)%len(self.circle)
                self.circle.insert(cidx, cm)

            print self.get_state(cp, cidx)

    def get_state(self, cp, cidx):
        circle = [str(v) for v in self.circle]
        circle[cidx] = "(%s)" % circle[cidx]
        return "[%d] %s" % (cp+1, " ".join(circle))


def _load_problem_data():
    with open("inputs/day09.txt") as f:
        instructions = []
        #example: 425 players; last marble is worth 70848 points
        for l in f.readlines():
            l = l.replace("players; last marble is worth", "").replace("points", "").split()
            nb_players = int(l[0])
            last_marble = int(l[1])
        return nb_players, last_marble


def get_winning_elf_score():
    nb_players, last_marble = _load_problem_data()

    game = Game(nb_players, last_marble)

    game.run()

    return max(game.players)


"""
--- Part Two ---

Amused by the speed of your answer, the Elves are curious:

What would the new winning Elf's score be if the number of the last marble were 100 times larger?
"""

class Node(object):
    def __init__(self, value, prevnode=None, nextnode=None):
        self.value = value
        self.prevnode = prevnode if prevnode is not None else self
        self.nextnode = nextnode if nextnode is not None else self

    def select_next(self, n):
        if n == 0:
            return self
        else:
            return self.nextnode.select_next(n-1)

    def select_previous(self, n):
        if n == 0:
            return self
        else:
            return self.prevnode.select_previous(n-1)

    def insert(self, value):
        newNode = Node(value, self, self.nextnode)  #create new node
        self.nextnode.prevnode = newNode
        self.nextnode = newNode #update next reference
        return newNode

    def pop(self):
        self.prevnode.nextnode = self.nextnode
        self.nextnode.prevnode = self.prevnode
        return self, self.nextnode


class CyclicGame(object):
    def __init__(self, nb_players):
        self.Nplayer = nb_players
        self.players = [0]*nb_players
        self.N0 = Node(0)
        self.current_N = self.N0


    def run(self, last_marble):
        for cm in range(1, last_marble + 1): #cm = current marble
            if cm%1000 == 0:
                print "%.2f%%" % (cm/float(last_marble)*100.0)

            cp = (cm-1) % self.Nplayer
            if cm % 23 == 0:
                pop_N, self.current_N = self.current_N.select_previous(7).pop()
                self.players[cp] += cm + pop_N.value
            else:
                self.current_N = self.current_N.select_next(1).insert(cm)

            #print "[%s] %s" % (cp+1, self.get_state())

    def get_state(self):
        state = "%s " % self.N0.value
        N = self.N0.nextnode
        while N != self.N0:
            if N == self.current_N:
                state += "(%s) " % N.value
            else:
                state += "%s " % N.value
            N = N.nextnode
        return state

def get_winning_elf_score_with_offset(offset=100):
    nb_players, last_marble = _load_problem_data()
    last_marble *= offset

    game = CyclicGame(nb_players)
    game.run(last_marble)

    return max(game.players)



if __name__ == '__main__':
    print("Part 1: get winning elf score: %s" % get_winning_elf_score())
    print("Part 2: get winning elf score with offset: %s" % get_winning_elf_score_with_offset())

