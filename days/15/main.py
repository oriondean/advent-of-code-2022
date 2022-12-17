from re import compile, Pattern
from collections import Counter
import time


def get_map(responses: list[list[(int, int)]]) -> dict[int, dict[int, str]]:
    map: dict[int, dict[int, str]] = {}
    rows = [[i[0][1], i[1][1]] for i in responses]
    dimensions_row = sorted([item for sublist in rows for item in sublist])

    for row in range(dimensions_row[0], dimensions_row[-1] + 1):
        map[row] = {}

    for response in responses:
        map[response[0][1]][response[0][0]] = 'S'
        map[response[1][1]][response[1][0]] = 'B'

    return map


def get_distance(source: (int, int), target: (int, int)) -> int:
    return abs(source[0] - target[0]) + abs(source[1] - target[1])


def get_bounding_box(position: (int, int), distance: int) -> list[(int, int)]:
    return [
        (position[0], position[1] - distance), (position[0] + distance, position[1]),
        (position[0], position[1] + distance), (position[0] - distance, position[1])
    ]


def get_adjacent_coords(box: list[(int, int)]) -> list[(int, int)]:
    coords = []
    width_middle = (box[1][0] - box[3][0]) + 1 + 2
    middle_col = (box[1][0] + box[3][0]) // 2
    range_width = list(range(1, width_middle, 2)) + list(range(width_middle, 0, -2))

    for row in range(box[0][1] - 1, box[2][1] + 2):
        range_halved = range_width.pop() // 2
        coords.append((middle_col - range_halved, row))
        if range_halved > 0:
            coords.append((middle_col + range_halved, row))

    return coords


def intersects_box(position: (int, int), box: list[(int, int)]) -> bool:
    if not (box[0][1] <= position[1] <= box[2][1] and box[3][0] <= position[0] <= box[1][0]):
        return False

    middle_col = (box[1][0] + box[3][0]) // 2
    middle_row = (box[0][1] + box[2][1]) // 2
    width_middle = (box[1][0] - box[3][0]) + 1
    width_pos = width_middle - (2 * (abs(position[1] - middle_row)))

    return (middle_col - (width_pos // 2)) <= position[0] <= middle_col + (width_pos // 2)


def mark_distance(map: dict[int, dict[int, str]], position: (int, int), distance: int, line_to_mark: int) -> None:
    for col in range(position[0] - distance, position[0] + distance + 1):
        if get_distance((col, line_to_mark), position) <= distance:
            if map[line_to_mark] is not None and map[line_to_mark].get(col) is None:
                map[line_to_mark][col] = '#'


def get_bordering_coordinates(borders_sensors: list[list[(int, int)]]) -> list[(int, int)]:
    coords = [get_adjacent_coords(borders) for borders in borders_sensors]
    print(f'\t timer: get adjacent coords {time.time() - time_start} seconds')
    coords = [item for sublist in coords for item in sublist]
    print(f'\t timer: flatten adjacent coords {time.time() - time_start} seconds')
    coords = [c for c in coords if 0 <= c[0] <= dimensions and 0 <= c[1] <= dimensions]
    print(f'\t timer: filter adjacent coords {time.time() - time_start} seconds')
    # We are assuming that the coordinate we need to find exists between two different sensor regions
    coords = [x for x, y in Counter(coords).items() if y > 1]
    print(f'\t timer: narrow onto dupes adjacent coords {time.time() - time_start} seconds')
    return coords
    # Less efficient but we can just dedupe the coordinates to check all potential places a beacon could be
    # return list(set(coords_to_check))


if __name__ == '__main__':
    regex_response: Pattern[str] = compile('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
    responses: list[list[(int, int)]] = []
    line_to_check: int = 2_000_000
    dimensions: int = 4_000_000
    time_start = time.time()

    with open('input.txt') as file:
        for line in file:
            line_parsed = [int(i) for i in regex_response.match(line.strip()).groups()]
            responses.append([(line_parsed[0], line_parsed[1]), (line_parsed[2], line_parsed[3])])
    file.close()
    print(f'\t timer: parse file {time.time() - time_start} seconds')

    map: dict[int, dict[int, str]] = get_map(responses)
    borders_sensors: list[list[(int, int)]] = []
    for i, response in enumerate(responses):
        distance = get_distance(response[0], response[1])
        mark_distance(map, response[0], distance, line_to_check)
        borders_sensors.append(get_bounding_box(response[0], distance))

    print('Part one', len([i for i in map[line_to_check] if map[line_to_check][i] == '#']))  # 5166077
    print(f'\t timer: part one {time.time() - time_start} seconds')

    for coord in get_bordering_coordinates(borders_sensors):
        if all([not intersects_box(coord, box) for box in borders_sensors]):
            # (3267801, 2703981) --> 13071206703981
            print('Part two', coord, (coord[0] * 4_000_000) + coord[1])
            break
    print(f'\t timer: part two {time.time() - time_start} seconds')