from functools import reduce
import re


def build_stacks(lines_stacks):
    max_line = len(max(lines_stacks))
    stack_count = max_line // 4
    stacks: list[list[str]] = [[] for _ in range(stack_count)]

    for col in range(1, max_line, 4):
        for line in lines_stacks:
            if len(line) >= col and line[col].isalnum():
                stacks[col // 4].insert(0, line[col])

    return stacks


def parse_command(input):
    return tuple(map(int, regex_command.match(input).groups()))


def build_commands(lines_commands):
    return list(map(parse_command, lines_commands))


def run_commands(lines_stacks, lines_commands, reverse_on_move):
    stacks: list[list[str]] = build_stacks(lines_stacks)
    commands: list[(int, int, int)] = build_commands(lines_commands)

    for command in commands:
        to_move: list[str] = stacks[command[1] - 1][-command[0]:]
        if reverse_on_move:
            to_move.reverse()

        stacks[command[1] - 1] = stacks[command[1] - 1][:-command[0]]
        stacks[command[2] - 1] = stacks[command[2] - 1] + to_move

    return stacks


if __name__ == '__main__':
    regex_command = re.compile('move (\d+) from (\d+) to (\d+)')

    with open('input.txt') as file:
        input: list[str] = file.readlines()
        file.close()

    separator: int = input.index('\n')
    lines_stacks: list[str] = input[:separator - 1]
    lines_commands: list[(int, int, int)] = input[separator + 1:]

    result_one = run_commands(lines_stacks, lines_commands, True)
    print('Part one', reduce(lambda memo, value: memo + value[len(value) - 1], result_one, ''))

    result_two = run_commands(lines_stacks, lines_commands, False)
    print('Part two', reduce(lambda memo, value: memo + value[len(value) - 1], result_two, ''))
