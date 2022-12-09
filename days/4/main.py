from functools import reduce


def parse_sections(to_parse):
    result = []

    for value in to_parse.split(','):
        pair = list(map(int, value.split('-')))
        result.append(range(pair[0], pair[1] + 1))

    return result


if __name__ == '__main__':
    with open('input.txt') as file:
        lines: list[str] = file.read().splitlines()
        input: list[[str, str]] = reduce(lambda memo, value: memo + [parse_sections(value)], lines, [])
        file.close()

    print('Part one',
          reduce(lambda memo, value: memo + int(set(value[0]).issubset(value[1]) or set(value[0]).issuperset(value[1])),
                 input, 0))

    print('Part two', reduce(lambda memo, value: memo + int(not set(value[0]).isdisjoint(value[1])), input, 0))
