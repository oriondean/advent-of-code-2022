from re import compile
from wraparound import wraparound_cube, wraparound_board
from bounds import get_bounds


def parse_directions(line: str) -> list:
    directions: list = []
    num: str = ''

    for char in line:
        if char.isnumeric():
            num += char
        else:
            directions.append(int(num))
            directions.append(char)
            num = ''
    if num:
        directions.append(int(num))

    return directions


def move(board: list[list[str]], regions: dict[str, (int, int)], regions_size: int, position: (int, int), facing: str,
         amount: int, is_cube: bool) -> ((int, int), str):
    (row, col) = position

    for _ in range(0, amount):
        row_next: int = row + (1 if facing == 'v' else -1 if facing == '^' else 0)
        col_next: int = col + (1 if facing == '>' else -1 if facing == '<' else 0)

        bounds_x: (int, int) = get_bounds(board[row])
        if col_next < bounds_x[0] or col_next > bounds_x[1]:
            ((row, col), facing) = wraparound_cube(board, regions, regions_size, (row, col), facing) if is_cube else\
                wraparound_board(board[row], (row, col), facing)
            continue

        row_y: list[str] = [row[col_next] if col_next < len(row) else '' for row in board]
        bounds_y: (int, int) = get_bounds(row_y)
        if row_next < bounds_y[0] or row_next > bounds_y[1]:
            ((row, col), facing) = wraparound_cube(board, regions, regions_size, (row, col), facing) if is_cube else\
                wraparound_board(row_y, (row, col_next), facing)
            continue

        if board[row_next][col_next] == '#':
            return (row, col), facing

        (row, col) = row_next, col_next

    return (row, col), facing


def rotate(facing: str, direction: str) -> str:
    facings = ['^', '>', 'v', '<']
    delta = 1 if direction == 'R' else -1

    return facings[(facings.index(facing) + delta) % len(facings)]


def trace_path(board: list[list[str]], directions: list[(int, str)], is_cube: bool) -> ((int, int), str):
    position: (int, int) = (0, board[0].index('.'))
    facing: str = '>'

    for direction in directions:
        if direction in ['L', 'R']:
            facing = rotate(facing, direction)
        else:
            (position, facing) = move(board, regions, regions_size, position, facing, direction, is_cube)

    return position, facing


if __name__ == '__main__':
    board: list[list[str]] = []
    regex_directions = compile('(\d+)(\w)')
    directions: list[(int, str)] = []
    values_facings: list[str] = ['>', 'v', '<', '^']
    regions_size: int = 50
    regions: dict[str, (int, int)] = {  # top left coords hand sourced from pattern in input
        'N': (regions_size, regions_size), 'E': (0, regions_size * 2),
        'S': (regions_size * 3, 0), 'W': (regions_size * 2, 0),
        'T': (0, regions_size), 'B': (regions_size * 2, regions_size)
    }

    with open('input.txt') as file:
        for line_raw in file:
            line: str = line_raw.rstrip()
            if '.' in line_raw:
                board.append(list(line))
            elif line:
                directions = parse_directions(line)
    file.close()

    (position, facing) = trace_path(board, directions, False)
    (position2, facing2) = trace_path(board, directions, True)

    print('Part one', ((position[0] + 1) * 1000) + ((position[1] + 1) * 4) + values_facings.index(facing), 65368)
    print('Part two', ((position2[0] + 1) * 1000) + ((position2[1] + 1) * 4) + values_facings.index(facing2), 156166)
