def draw_path(map: list[list[str]], position_start: (int, int), position_end: (int, int)) -> None:
    diff_row = position_start[1] - position_end[1]
    diff_col = position_start[0] - position_end[0]

    if diff_col != 0:
        delta = -1 if diff_col > 0 else 1
        for col in range(position_start[0], position_end[0] + delta, delta):
            map[position_start[1]][col] = '#'
    elif diff_row != 0:
        delta = -1 if diff_row > 0 else 1
        for row in range(position_start[1], position_end[1] + delta, delta):
            map[row][position_start[0]] = '#'


def draw_paths(map: list[list[str]], paths: list[list[(int, int)]]) -> None:
    for coords in paths:
        for i, coord in enumerate(coords[1:]):
            draw_path(map, coords[i], coords[i + 1])


def create_map(size: int, paths: list[list[(int, int)]], position_sand_spout: (int, int), include_floor: bool) -> list[list[str]]:
    map: list[list[str]] = [['.' for __ in range(size)] for _ in range(size)]
    floor = [(i, 2 + sorted([c[1] for coords in paths for c in coords])[-1]) for i in
             range(size)] if include_floor else []

    draw_paths(map, paths + [floor])
    map[position_sand_spout[0]][position_sand_spout[1]] = '+'

    return map


def move_sand(map: list[list[str]], pos: (int, int)) -> (int, int):
    col, row = pos

    if map[row + 1][col] == '.':
        return col, row + 1
    elif map[row + 1][col - 1] == '.':
        return col - 1, row + 1
    elif map[row + 1][col + 1] == '.':
        return col + 1, row + 1

    return pos


def simulate_sand_movements(map: list[list[str]], position_sand_spout: (int, int), limit_moves: int) -> int:
    units_dropped: int = 0

    while True:
        is_moving: bool = True
        position_sand: (int, int) = position_sand_spout
        count_moves: int = 0

        while is_moving:
            pos_sand_new = move_sand(map, position_sand)
            is_moving = position_sand != pos_sand_new
            position_sand = pos_sand_new
            count_moves += 1

            if count_moves >= limit_moves or position_sand == position_sand_spout:
                return units_dropped

        map[position_sand[1]][position_sand[0]] = 'o'
        units_dropped += 1


if __name__ == '__main__':
    paths: list[list[(int, int)]] = []

    with open('input.txt') as file:
        for line in file:
            paths.append([tuple([int(j) for j in i.split(',')]) for i in line.split(' -> ')])

    position_sand_spout: (int, int) = (500, 0)
    map: list[list[str]] = create_map(1_000, paths, position_sand_spout, False)
    map_with_floor: list[list[str]] = create_map(1_000, paths, position_sand_spout, True)

    print('Part one', simulate_sand_movements(map, position_sand_spout, 500))
    print('Part two', simulate_sand_movements(map_with_floor, position_sand_spout, 500) + 1)
