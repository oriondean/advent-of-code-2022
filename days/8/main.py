def is_visible(map, row, col) -> bool:
    value: int = map[row][col]

    if all([map[x][col] < value for x in range(row - 1, -1, -1)]):
        return True
    elif all([map[x][col] < value for x in range(row + 1, len(map), 1)]):
        return True
    elif all([map[row][x] < value for x in range(col - 1, -1, -1)]):
        return True
    elif all([map[row][x] < value for x in range(col + 1, len(map[0]), 1)]):
        return True

    return False


def count_trees_visible(map, row, col) -> int:
    value: int = map[row][col]

    try:
        seen_top: int = [map[x][col] < value for x in range(row - 1, -1, -1)].index(False) + 1
    except ValueError:
        seen_top: int = len([map[x][col] < value for x in range(row - 1, -1, -1)])

    try:
        seen_bottom: int = [map[x][col] < value for x in range(row + 1, len(map), 1)].index(False) + 1
    except ValueError:
        seen_bottom: int = len([map[x][col] < value for x in range(row + 1, len(map), 1)])

    try:
        seen_left: int = [map[row][x] < value for x in range(col - 1, -1, -1)].index(False) + 1
    except ValueError:
        seen_left: int = len([map[row][x] < value for x in range(col - 1, -1, -1)])

    try:
        seen_right: int = [map[row][x] < value for x in range(col + 1, len(map[0]), 1)].index(False) + 1
    except ValueError:
        seen_right: int = len([map[row][x] < value for x in range(col + 1, len(map[0]), 1)])

    return seen_top * seen_bottom * seen_left * seen_right


if __name__ == '__main__':
    with open('input.txt') as file:
        map: list[list[int]] = [list(map(int, list(x))) for x in file.read().splitlines()]
        file.close()

    count_rows: int = len(map)
    count_cols: int = len(map[0])
    count_visible: int = 0
    highest_seen = 0

    for row in range(count_rows):
        for col in range(count_cols):
            if row in [0, count_rows - 1] or col in [0, count_cols - 1] or is_visible(map, row, col):
                count_visible += 1

            if count_trees_visible(map, row, col) > highest_seen:
                highest_seen = count_trees_visible(map, row, col)

    print('Part one', count_visible)
    print('Part two', highest_seen)
