from collections import deque
from functools import reduce
from re import compile, Pattern
from time import time


def parse_blueprint(line: str) -> tuple:
    parsed = regex_blueprint.match(line).groups()
    robot_ore = int(parsed[1])
    robot_clay = int(parsed[2])
    robot_obsidian = tuple(map(int, parsed[3:5]))
    robot_geode = tuple(map(int, parsed[5:7]))

    # optimisation - find out maximum amount you can spend per tick
    max_spend = (max(robot_ore, robot_clay, robot_obsidian[0], robot_geode[0]), robot_obsidian[1], robot_geode[1])
    return int(parsed[0]), robot_ore, robot_clay, *robot_obsidian, *robot_geode, *max_spend


def get_possible_decisions(blueprint: tuple, tick: int, robots: (int, int, int, int), counts: (int, int, int, int),
                           highest_seen: dict[int, int], time_max: int) -> deque[(int, int, int, int)]:
    decisions: deque[(int, int, int, int)] = deque()
    can_build_geode_robot: bool = robots[2] > 0 and counts[0] >= blueprint[5] and counts[2] >= blueprint[6]
    ample_time: int = (time_max - tick) > 5

    # optimisation - if we can build a geode robot then only do so
    if can_build_geode_robot:
        return deque([(0, 0, 0, 1)])
    # optimisation - don't build obsidian robot if we don't have clay robots
    if robots[1] > 0 and counts[0] >= blueprint[3] and counts[1] >= blueprint[4] and robots[2] < blueprint[9]:
        decisions.append((0, 0, 1, 0))
    # optimisation - don't build ore / clay robots near end of run
    if ample_time and counts[0] >= blueprint[2] and robots[1] < blueprint[8]:
        decisions.append((0, 1, 0, 0))
    if ample_time and counts[0] >= blueprint[1] and robots[0] < blueprint[7]:
        decisions.append((1, 0, 0, 0))

    time_left = time_max - tick

    # optimisation - if you can't hit max seen geodes despite building geode robot each turn then end branch
    if (counts[3] + (robots[3] * time_left) + (time_left * (time_left + 1) // 2)) <= highest_seen.get(time_max - 1, 0):
        return deque()

    decisions.append((0, 0, 0, 0))
    return decisions


def get_state(blueprint: tuple, decision: (int, int, int, int), robots: tuple, counts: tuple) -> (tuple, tuple):
    robots_new: (int, int, int, int) = robots
    counts_new: (int, int, int, int) = counts

    if decision == (1, 0, 0, 0):
        robots_new = (robots[0] + 1, robots[1], robots[2], robots[3])
        counts_new = (counts[0] - blueprint[1], counts[1], counts[2], counts[3])
    elif decision == (0, 1, 0, 0):
        robots_new = (robots[0], robots[1] + 1, robots[2], robots[3])
        counts_new = (counts[0] - blueprint[2], counts[1], counts[2], counts[3])
    elif decision == (0, 0, 1, 0):
        robots_new = (robots[0], robots[1], robots[2] + 1, robots[3])
        counts_new = (counts[0] - blueprint[3], counts[1] - blueprint[4], counts[2], counts[3])
    elif decision == (0, 0, 0, 1):
        robots_new = (robots[0], robots[1], robots[2], robots[3] + 1)
        counts_new = (counts[0] - blueprint[5], counts[1], counts[2] - blueprint[6], counts[3])

    return robots_new,\
        (counts_new[0] + robots[0], counts_new[1] + robots[1], counts_new[2] + robots[2], counts_new[3] + robots[3])


def run_decision(blueprint: tuple, robots: tuple, counts: tuple, decision: tuple, tick: int, time_max: int) -> tuple:
    robots_new, counts_new = get_state(blueprint, decision, robots, counts)

    time_left = time_max - tick
    # optimisation - cap the counts to the max you can spend in the time remaining (reduces number of states)
    if counts_new[0] > blueprint[7] * time_left:
        counts_new = (blueprint[7] * time_left, counts_new[1], counts_new[2], counts_new[3])
    if counts_new[1] > blueprint[8] * time_left:
        counts_new = (counts_new[0], blueprint[8] * time_left, counts_new[2], counts_new[3])
    if counts_new[2] > blueprint[9] * time_left:
        counts_new = (counts_new[0], counts_new[1], blueprint[9] * time_left, counts_new[3])

    return robots_new, counts_new


def find_best_plan(blueprint: tuple, time_max: int) -> int:
    state_start: tuple = (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    visited: set[tuple] = set(state_start)
    queue: deque = deque([state_start])
    highest_seen: dict[int, int] = {}

    while queue:
        state = queue.popleft()
        decisions = get_possible_decisions(blueprint, state[0], state[1:5], state[5:9], highest_seen, time_max)

        for i, decision in enumerate(decisions):
            (robots_new, counts_new) = run_decision(blueprint, state[1:5], state[5:9], decision, state[0], time_max)

            if counts_new[3] > highest_seen.get(state[0], 0):
                highest_seen[state[0]] = counts_new[3]

            state_new: tuple = (state[0] + 1, *robots_new, *counts_new, decision)
            if state_new not in visited and state_new[0] < time_max:
                queue.append(state_new)
                visited.add(state_new)

    return highest_seen.get(time_max - 1, 0)


if __name__ == '__main__':
    time_start: float = time()
    regex_blueprint: Pattern[str] = compile(
        'Blueprint (\d+): Each ore robot costs (\d+) ore. ' +
        'Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. ' +
        'Each geode robot costs (\d+) ore and (\d+) obsidian'
    )

    with open('input.txt') as file:
        blueprints = [parse_blueprint(line) for line in file.read().splitlines()]
    file.close()

    result_one: int = reduce(lambda memo, value: memo + (value[0] * find_best_plan(value, 25)), blueprints, 0)
    print(f'({time() - time_start:.2f}s) Part one {result_one}')

    result_two: int = reduce(lambda memo, value: memo * find_best_plan(value, 33), blueprints[:3], 1)
    print(f'({time() - time_start:.2f}s) Part two {result_two}')
