from copy import deepcopy
from functools import reduce
from typing import Callable

from monkey import Monkey


def parse_input(file) -> list[Monkey]:
    monkeys: list[Monkey] = []
    current_monkey = None

    for line_raw in file:
        line: str = line_raw.strip()

        if line.startswith('Monkey'):
            current_monkey = Monkey()
        elif line.startswith('Starting items:'):
            current_monkey.items = list(map(int, line.split(': ')[1].split(', ')))
        elif line.startswith('Operation:'):
            operation = line.split('new = ')[1]
            current_monkey.operation_raw = operation
            current_monkey.operation = \
                lambda operation, value: eval(operation, {'__builtins__': None}, {'old': value})
        elif line.startswith('Test:'):
            current_monkey.test_divisible_by = int(line.split('by ')[1])
        elif line.startswith('If true:'):
            current_monkey.test_pass_target = int(line.split('monkey ')[1])
        elif line.startswith('If false:'):
            current_monkey.test_fail_target = int(line.split('monkey ')[1])
            monkeys.append(current_monkey)

    return monkeys


def run_rounds(monkeys_initial: list[Monkey], round_count: int, modifier_worry: Callable[[int], int]) -> list[Monkey]:
    monkeys: list[Monkey] = deepcopy(monkeys_initial)
    for i in range(0, round_count):
        for m, monkey in enumerate(monkeys):
            monkey.inspection_count += len(monkey.items)
            for item in monkey.items:
                (target_throw, new_item) = monkey.inspect(item, modifier_worry)
                monkeys[target_throw].items.append(new_item)
            monkey.items = []

    return monkeys


if __name__ == '__main__':
    with open('input.txt') as file:
        monkeys: list[Monkey] = parse_input(file)
        file.close()

    monkeys_one: list[Monkey] = run_rounds(monkeys, 20, lambda value: value // 3)
    active_most: list[Monkey] = sorted(monkeys_one, key=lambda monkey: monkey.inspection_count, reverse=True)[:2]
    print('Part one', active_most[0].inspection_count * active_most[1].inspection_count)

    least_common_multiple: int = reduce(lambda memo, value: memo * value.test_divisible_by, monkeys, 1)
    monkeys_two: list[Monkey] = run_rounds(monkeys, 10_000, lambda value: value % least_common_multiple)
    active_most: list[Monkey] = sorted(monkeys_two, key=lambda monkey: monkey.inspection_count, reverse=True)[:2]
    print('Part two', active_most[0].inspection_count * active_most[1].inspection_count)
