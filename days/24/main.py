import sys
from copy import deepcopy
from collections import deque


def is_within_bounds(x: int, y: int, bounds: (int, int)) -> bool:
    if (x, y) in [(0, 1), (bounds[0], bounds[1] - 1)]:
        return True
    return 0 < x < bounds[0] and 0 < y < bounds[1]


def get_move(blizzard: (int, int, str), bounds: (int, int)) -> (int, int, str):
    moves: dict[str, (int, int)] = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
    facing: str = blizzard[2]
    position: (int, int) = blizzard[0] + moves[facing][0], blizzard[1] + moves[facing][1]

    if not is_within_bounds(*position, bounds):
        delta_new: int = 1 if facing in ['>', 'v'] else bounds[1] - 1 if facing == '<' else bounds[0] - 1
        return (position[0], delta_new, facing) if facing in ['<', '>'] else (delta_new, position[1], facing)

    return *position, facing


def move_blizzards(map: list[list[str]], blizzards: list[(int, int)], blizzard_chars: set[str]) -> list[(int, int)]:
    blizzards_moved: list[(int, int)] = []

    for blizzard in blizzards:
        blizzards_moved.append(get_move(blizzard, map_bounds))
        map[blizzard[0]][blizzard[1]] = '.'

    for blizzard in blizzards_moved:
        (x, y, facing) = blizzard
        map[x][y] = facing if map[x][y] == '.' else '2' if map[x][y] in blizzard_chars else str(int(map[x][y]) + 1)

    return blizzards_moved


def get_moves(x: int, y: int, bounds: (int, int)) -> list[(int, int)]:
    neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x, y)]
    return [position for position in neighbours if is_within_bounds(*position, bounds)]


def is_safe_move(map: list[list[str]], neighbour: (int, int)) -> bool:
    return map[neighbour[0]][neighbour[1]] == '.'


def find_shortest_path(maps: list[list[list[str]]], bounds: (int, int), start: (int, int), end: (int, int)):
    results: dict[str, int] = dict()
    to_visit: deque[(int, int, int)] = deque([(*start, 0)])
    visited: set[(int, int, int)] = {(*start, 0)}

    while to_visit:
        (x, y, turn) = to_visit.popleft()

        value: int = results.get(str((x, y)), sys.maxsize)
        results[str((x, y))] = turn if turn < value else value
        if (x, y) == end:
            return results.get((str(end)))

        for neighbour in get_moves(x, y, bounds):
            if (*neighbour, turn + 1) not in visited and is_safe_move(maps[turn + 1], neighbour):
                to_visit.append((neighbour[0], neighbour[1], turn + 1))
                visited.add((*neighbour, turn + 1))


if __name__ == '__main__':
    map: list[list[str]] = []
    blizzards: list[(int, int, str)] = []
    blizzard_chars: set[str] = {'<', '>', 'v', '^'}

    with open('input.txt') as file:
        for i, row in enumerate(file.read().splitlines()):
            map.append(list(row))
            blizzards += [(i, *x) for x in enumerate(row) if row[x[0]] in blizzard_chars]
        file.close()

    map_bounds: (int, int) = (len(map) - 1, len(map[0]) - 1)
    map_top: (int, int) = (0, 1)
    map_bottom: (int, int) = (map_bounds[0], map_bounds[1] - 1)
    maps: list[list[list[str]]] = []
    while map not in maps:
        maps.append(deepcopy(map))
        blizzards = move_blizzards(map, blizzards, blizzard_chars)

    results: list[int] = [find_shortest_path(maps, map_bounds, map_top, map_bottom)]
    print('Part one', sum(results))

    maps = maps[(results[-1] % len(maps)):] + maps[0: (results[-1] % len(maps))]
    results.append(find_shortest_path(maps, map_bounds, map_bottom, map_top))
    maps = maps[(results[-1] % len(maps)):] + maps[0: (results[-1] % len(maps))]
    results.append(find_shortest_path(maps, map_bounds, map_top, map_bottom))
    print('Part two', sum(results))
