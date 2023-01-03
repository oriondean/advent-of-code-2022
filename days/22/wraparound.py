from bounds import get_bounds


def find_border(regions: dict[str, (int, int)], size_region: int, position: (int, int)) -> str:
    return [b[0] for b in regions.items() if
            0 <= (position[0] - b[1][0]) < size_region and 0 <= (position[1] - b[1][1]) < size_region][0]


def wraparound_cube(board: list[list[str]], regions: dict[str, (int, int)], size_region: int, position: (int, int), facing: str) -> ((int, int), str):
    border: (int, int) = find_border(regions, size_region, position)
    position_new: (int, int) = (0, 0)
    size: int = size_region - 1

    if border == 'T':
        if facing == '^':
            row_new = regions['S'][0] + (position[1] - regions['T'][1])
            col_new = regions['S'][1]
            position_new = (row_new, col_new), '>'
        elif facing == '<':
            row_new = (regions['W'][0] + size) - (position[0] - regions['T'][0])
            col_new = regions['W'][1]
            position_new = (row_new, col_new), '>'
    elif border == 'E':
        if facing == '^':
            row_new = regions['S'][0] + size
            col_new = regions['S'][1] + (position[1] - regions['E'][1])
            position_new = (row_new, col_new), '^'
        elif facing == '>':
            row_new = (regions['B'][0] + size) - (position[0] - regions['E'][0])
            col_new = regions['B'][1] + size
            position_new = (row_new, col_new), '<'
        elif facing == 'v':
            row_new = regions['N'][0] + (position[1] - regions['E'][1])
            col_new = regions['N'][1] + size
            position_new = (row_new, col_new), '<'
    elif border == 'N':
        if facing == '<':
            row_new = regions['W'][0]
            col_new = regions['W'][1] + (position[0] - regions['N'][0])
            position_new = (row_new, col_new), 'v'
        elif facing == '>':
            row_new = regions['E'][0] + size
            col_new = regions['E'][1] + (position[0] - regions['N'][0])
            position_new = (row_new, col_new), '^'
    elif border == 'W':
        if facing == '^':
            row_new = regions['N'][0] + (position[1] - regions['W'][1])
            col_new = regions['N'][1]
            position_new = (row_new, col_new), '>'
        elif facing == '<':
            row_new = (regions['T'][0] + size) - (position[0] - regions['W'][0])
            col_new = regions['T'][1]
            position_new = (row_new, col_new), '>'
    elif border == 'B':
        if facing == '>':
            row_new = (regions['E'][0] + size) - (position[0] - regions['B'][0])
            col_new = regions['E'][1] + size
            position_new = (row_new, col_new), '<'
        elif facing == 'v':
            row_new = regions['S'][0] + (position[1] - regions['B'][1])
            col_new = regions['S'][1] + size
            position_new = (row_new, col_new), '<'
    elif border == 'S':
        if facing == '>':
            row_new = regions['B'][0] + size
            col_new = regions['B'][1] + (position[0] - regions['S'][0])
            position_new = (row_new, col_new), '^'
        elif facing == 'v':
            row_new = regions['E'][0]
            col_new = regions['E'][1] + (position[1] - regions['S'][1])
            position_new = (row_new, col_new), 'v'
        elif facing == '<':
            row_new = regions['T'][0]
            col_new = regions['T'][1] + (position[0] - regions['S'][0])
            position_new = (row_new, col_new), 'v'

    return (position, facing) if board[position_new[0][0]][position_new[0][1]] == '#' else position_new


def wraparound_board(line: list[str], position: (int, int), facing: str) -> ((int, int), str):
    (row, col) = position
    bounds: (int, int) = get_bounds(line)

    if facing == '<' or facing == '>':
        col_new = bounds[0] if facing == '>' else bounds[1]
        return (position, facing) if line[col_new] == '#' else ((row, col_new), facing)
    else:
        row_new = bounds[0] if facing == 'v' else bounds[1]
        return (position, facing) if line[row_new] == '#' else ((row_new, col), facing)
