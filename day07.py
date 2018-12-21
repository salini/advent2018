
"""
--- Day 7: The Sum of Its Parts ---

You find yourself standing on a snow-covered coastline; apparently, you landed a little off course.
The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore.
It's quite cold out, so you decide to risk creating a paradox by asking them for directions.
"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish.
Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment.
You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions."
It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input).
Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.

Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----

Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

    Only C is available, and so it is done first.
    Next, both A and F are available. A is first alphabetically, so it is done next.
    Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
    After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
    F is the only choice, so it is done next.
    Finally, E is completed.

So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
"""

from advent.log import show_log, log

class Instruction(object):
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def __repr__(self):
        return "%s -> %s" % (self.parent, self.child)

class Node(object):
    def __init__(self, name):
        self.name = name
        self.parents = set()
        self.children = set()
        self.value = None

    def add_child(self, child):
        self.children.add(child)
        child.parents.add(self)

    def has_parents(self):
        return True if len(self.parents) else False

    def __repr__(self):
        return "%s ==> %s (%s) ==>%s" % ([p.name for p in self.parents], self.name, self.value, [c.name for c in self.children])


class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_instruction(self, instruction):
        P = instruction.parent
        C = instruction.child
        if P not in self.nodes:
            self.nodes[P] = Node(P)
        if C not in self.nodes:
            self.nodes[C] = Node(C)

        self.nodes[P].add_child(self.nodes[C])

    def del_node(self, node):
        n = self.nodes[node]
        for p in n.parents:
            p.children.remove(n)
        for c in n.children:
            c.parents.remove(n)
        del self.nodes[node]

    def get_heads(self):
        heads = {}
        for k, v in self.nodes.items():
            if len(v.parents) == 0:
                heads[k] = v
        return heads

    def __repr__(self):
        return "\n".join(str(n) for n in self.nodes.values())


def _load_instructions():
    with open("inputs/day07.txt") as f:
        instructions = []
        #example: Step F must be finished before step Q can begin.
        for l in f.readlines():
            l = l.replace("Step", "").replace("must be finished before step", "").replace("can begin.", "")
            instructions.append(Instruction(*l.split()))
        return instructions


def get_ordered_instructions():
    instructions = _load_instructions()

    g = Graph()
    for i in instructions:
        g.add_instruction(i)

    ordered_instruction = ""
    while len(g.nodes):
        heads = g.get_heads()
        h = list(heads.keys())
        h.sort()
        ordered_instruction += h[0]
        log(ordered_instruction)
        g.del_node(h[0])

    return ordered_instruction




"""
--- Part Two ---

As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together."
Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.
To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds).
Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second.
Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""

class Task(object):
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def process(self, t):
        self.time -= t


class PoolOfWorker(object):
    def __init__(self, nbworker):
        self.workers = [None]*nbworker

    def nb_worker_available(self):
        return self.workers.count(None)

    def get_available_worker_index(self):
        return self.workers.index(None) if None in self.workers else None

    def add_node_as_task(self, node):
        self.add_task(Task(node.name, node.value))

    def has_tasks_in_process(self):
        return (len(self.get_current_tasks()) != 0)

    def add_task(self, task):
        idx = self.get_available_worker_index()
        log("assign %s (%d) to worker '%d'" % (task.name, task.time, idx))
        self.workers[idx] = task

    def get_current_tasks(self):
        return [t for t in self.workers if t is not None]

    def get_time_to_finish_next_task(self):
        tasks = self.get_current_tasks()
        return min([t.time for t in tasks])

    def process(self, t):
        for task in self.get_current_tasks():
            task.process(t)

    def process_until_one_finishes(self):
        t = self.get_time_to_finish_next_task()
        self.process(t)
        return t

    def del_finished(self):
        task_finished = []
        for idx in range(len(self.workers)):
            if self.workers[idx] is not None and self.workers[idx].time == 0:
                log("worker '%d' completed %s" % (idx, self.workers[idx].name))
                task_finished.append(self.workers[idx].name)
                self.workers[idx] = None

        return task_finished


def get_time_to_complete():
    instructions = _load_instructions()

    g = Graph()
    for i in instructions:
        g.add_instruction(i)

    for k, v in g.nodes.items():
        v.value = (ord(k)-64) + 60

    T = 0
    pool = PoolOfWorker(5)

    while len(g.nodes) or pool.has_tasks_in_process():
        log("=========== time: %d =============" % T)
        log("remaining: %s (%d)" % (",".join(g.nodes.keys()), len(g.nodes.keys())))
        log("in process: %s" % [(t.name, t.time)for t in pool.get_current_tasks()])
        heads = g.get_heads()
        sheads = heads.keys()
        sheads.sort()
        for task in pool.get_current_tasks():
            if task.name in sheads:
                sheads.remove(task.name)
        log("head tasks: %s || available workers: %d" % (sheads, pool.nb_worker_available()))

        log("--- assign ------------------")
        while len(sheads) and pool.nb_worker_available():
            nname = sheads.pop(0)
            pool.add_node_as_task(heads[nname])

        log("--- process ------------------")
        t = pool.process_until_one_finishes()
        T += t
        ## one can also do step by step:
        #pool.process(1)
        #T += 1

        log("--- delete completed ------------------")
        task_finished = pool.del_finished()
        for tname in task_finished:
            g.del_node(tname)

    log("Final time: %d" % T)
    return T


def check():
    print("- Part 1: {0}".format(get_ordered_instructions()=="ADEFKLBVJQWUXCNGORTMYSIHPZ")) #Your puzzle answer was ADEFKLBVJQWUXCNGORTMYSIHPZ.
    print("- Part 2: {0}".format(get_time_to_complete()==1120)) #Your puzzle answer was 1120.


if __name__ == '__main__':
    show_log(True)
    print("Part 1: get ordered instructions: %s" % get_ordered_instructions())
    print("Part 2: get time to complete: %s" % get_time_to_complete())

