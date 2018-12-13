"""
--- Day 4: Repose Record ---

You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab.
You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in.
Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post!
They've been writing down the ID of the one guard on duty that night -
the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up

Timestamps are written using year-month-day hour:minute format.
The guard falling asleep or waking up is always the one whose shift most recently started.
Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....

The columns are Date, which shows the month-day portion of the relevant day;
ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour.
(The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up.
For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in.
You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10).
Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them.
You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)
"""

import numpy as np

from datetime import datetime

class Log(object):
    def __init__(self, line):
        time, sep, msg = line.partition("]")
        self.time = time.strip()[1:] #remove "["
        self.msg = msg.strip()

    def __repr__(self):
        return self.time + ": "+self.msg

class SleepPeriod(object):
    def __init__(self, start, end):
        fmt = '%Y-%m-%d %H:%M'
        self.s = datetime.strptime(start, fmt)
        self.e = datetime.strptime(end, fmt)
        #sleeps are always between 00:00 and 00:59, so only minutes are releavant
        self.sleep_range = np.zeros(60)
        self.sleep_range[self.s.minute:self.e.minute] = 1


class Shift(object):
    def __init__(self, guard):
        self.logs = []
        self.guard = guard
        self.sleeps = []

    def add(self, log):
        self.logs.append(log)

    def compute_sleeps(self):
        # assert it is always guard first, then odds "falls asleep", even "wakes up"
        assert(len(self.logs)%2==1)
        assert("Guard #" in self.logs[0].msg)
        assert(all(["falls asleep" in l.msg for l in self.logs[1::2]]))
        assert(all(["wakes up" in l.msg for l in self.logs[2::2]]))

        self.sleeps = [SleepPeriod(start.time, end.time) for start, end in zip(self.logs[1::2], self.logs[2::2])]


def _get_ordered_log():
    with open("inputs/day04.txt") as f:
        logs = [Log(l) for l in f.readlines()]
    logs.sort(key=lambda x: x.time)      #sort by time
    return logs



def _get_guards_shifts(ord_logs):
    # regroup logs to get shifts
    shifts = []
    for l in ord_logs:
        if l.msg.strip().lower().startswith("guard #"):
            guard = int(l.msg.partition("#")[2].split()[0])
            shifts.append(Shift(guard))

        shifts[-1].add(l)

    return shifts


def _get_guard_sleeps(shifts):
    guard_sleeps = {}
    for s in shifts:
        s.compute_sleeps()
        if s.guard not in guard_sleeps:
            guard_sleeps[s.guard] = []
        guard_sleeps[s.guard].extend(s.sleeps)

    guard_total_sleeps = {}
    for k,list_of_sleeps in guard_sleeps.items():
        sleep_range = np.zeros(60)
        for s in list_of_sleeps:
            sleep_range += s.sleep_range

        guard_total_sleeps[k] = sleep_range

    return guard_total_sleeps


def get_guard_most_asleep_and_minute():
    ord_logs =_get_ordered_log()
    shifts = _get_guards_shifts(ord_logs)
    guard_total_sleeps = _get_guard_sleeps(shifts)

    guard, sleep_range = max(guard_total_sleeps.items(), key=lambda x: sum(x[1]))
    min_arg_max = np.argmax(sleep_range)
    return guard * min_arg_max




"""
--- Part Two ---

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total.
(In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
"""

def get_guard_asleep_regularly_and_minute():
    ord_logs =_get_ordered_log()
    shifts = _get_guards_shifts(ord_logs)
    guard_total_sleeps = _get_guard_sleeps(shifts)

    guard, sleep_range = max(guard_total_sleeps.items(), key=lambda x: max(x[1]))
    min_arg_max = np.argmax(sleep_range)
    return guard * min_arg_max


if __name__ == '__main__':
    print("Part 1: get guard and minute: %d" % get_guard_most_asleep_and_minute())
    print("Part 2: get guard sleeping regularly at same time: %s" % get_guard_asleep_regularly_and_minute())

