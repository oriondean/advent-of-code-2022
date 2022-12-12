from string import ascii_letters
from functools import reduce


def is_valid_move(area: list[list[str]], source: (int, int), target: (int, int)) -> bool:
    (t0, t1) = target
    if not (t0 >= 0 and t1 >= 0 and (t0 <= len(area) - 1) and (t1 <= len(area[0]) - 1)):
        return False
    return ascii_letters.index(area[t0][t1]) <= ascii_letters.index(area[source[0]][source[1]]) + 1


def get_valid_moves(area: list[list[str]], seen, position: (int, int), start) -> list[(int, int)]:
    (row, col) = position
    moves = list(filter(lambda value: value != start and str(value) not in seen.keys(),
                        [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]))
    return reduce(lambda memo, value: memo + [value] if is_valid_move(area, position, value) else memo, moves, [])


def pathfinder(area: list[list[str]], start, end) -> int:
    seen = {str(start): 0}
    moves = [start]
    distance = 0

    while len(moves) > 0 and str(end) not in seen.keys():
        valid_moves = list(map(lambda value: get_valid_moves(area, seen, value, start), moves))
        moves = list(set([item for sublist in valid_moves for item in sublist]))
        for move in moves:
            seen[str(move)] = distance + 1
        distance += 1

    return seen.get(str(end)) if str(end) in seen.keys() else -1


if __name__ == '__main__':
    area: list[list[str]] = []
    start = (-1, -1)
    end = (-1, -1)
    elevations_lowest = []

    with open('input.txt') as file:
        for line_raw in file:
            line = line_raw.strip()

            if 'S' in line:
                start: (int, int) = len(area), line.index('S')
                line = line.replace('S', 'a')
            if 'E' in line:
                end: (int, int) = len(area), line.index('E')
                line = line.replace('E', 'z')
            if 'a' in line:
                elevations_lowest += [(len(area), c) for c, x in enumerate(line) if x == 'a']

            area.append(list(line))

        file.close()

    print('Part one', pathfinder(area, start, end))
    results = map(lambda value: pathfinder(area, value, end), elevations_lowest)
    print('Part two', sorted(filter(lambda value: value != -1, results))[0])
