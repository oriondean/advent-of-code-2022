from functools import reduce
from string import ascii_letters


def split_list(to_split) -> tuple:
    half: int = len(to_split) // 2
    return to_split[:half], to_split[half:]


def calculate_priority(*args) -> int:
    common_letter: str = reduce(lambda memo, value: memo.intersection(value), args[1:], set(args[0])).pop()
    return ascii_letters.index(common_letter) + 1


if __name__ == '__main__':
    with open('input.txt') as file:
        rucksacks: list[str] = file.read().splitlines()
        file.close()

    compartments: list[(str, str)] = reduce(lambda memo, value: memo + [split_list(value)], rucksacks, [])
    partition_size: int = 3
    grouped_rucksacks: list[(str, str, str)] = \
        [rucksacks[i: i + partition_size] for i in range(0, len(rucksacks), partition_size)]

    print('Part one',
          reduce(lambda memo, value: memo + calculate_priority(value[0], value[1]), compartments, 0))
    print('Part two',
          reduce(lambda memo, value: memo + calculate_priority(value[0], value[1], value[2]), grouped_rucksacks, 0))
