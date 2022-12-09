from functools import reduce


def group_calories(memo, value) -> list[int]:
    if value in ['', '\n']:
        return memo + [0]
    return memo[:-1] + [memo[len(memo) - 1] + int(value)]


if __name__ == '__main__':
    with open('input.txt') as file:
        result = reduce(group_calories, file, [0])
        file.close()

    print('Part one', max(result))
    print('Part two', sum(sorted(result)[-3:]))
