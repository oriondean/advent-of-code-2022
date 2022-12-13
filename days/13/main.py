from functools import cmp_to_key


def partition(list, n):
    for i in range(0, len(list), n):
        yield list[i: i + n]


def compare_list(a, b) -> int:
    index = 0
    while index < min(len(a), len(b)):
        result = compare(a[index], b[index])
        if result != 0:
            return result
        index += 1

    return len(b) - len(a)


def compare(a, b) -> int:
    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    elif isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    elif isinstance(a, int) and isinstance(b, int):
        return b - a
    elif isinstance(a, list) and isinstance(b, list):
        return compare_list(a, b)


if __name__ == '__main__':
    with open('input.txt') as file:
        packets = [eval(line, {'__builtins__': None}, {}) for line in file.read().splitlines() if line != '']
        pairs = partition(packets, 2)
    file.close()

    print('Part one', sum([i + 1 for i, pair in enumerate(pairs) if compare(pair[0], pair[1]) > 0]))

    results = sorted(packets + [[[2]], [[6]]], key=cmp_to_key(compare), reverse=True)
    print('Part two', (results.index([[2]]) + 1) * (results.index([[6]]) + 1))
