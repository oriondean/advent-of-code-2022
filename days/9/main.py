def parse_line(line) -> (str, int):
    (direction, amount) = line.split(' ')
    return direction, int(amount)


def move_head(direction, position) -> (str, int):
    if direction in ['L', 'R']:
        return position[0], position[1] + (1 if direction == 'R' else -1)
    elif direction in ['U', 'D']:
        return position[0] + (1 if direction == 'D' else -1), position[1]


def move_tail(position_head, position_tail) -> (str, int):
    [row, col] = position_tail

    #  if head is two steps away in a single direction, move one step towards it
    if position_head == (row - 2, col):
        return row - 1, col
    if position_head == (row + 2, col):
        return row + 1, col
    if position_head == (row, col - 2):
        return row, col - 1
    if position_head == (row, col + 2):
        return row, col + 1

    # if head is two steps away across two directions, move diagonally towards it
    elif position_head in [(row - 2, col - 1), (row - 1, col - 2), (row - 2, col - 2)]:
        return row - 1, col - 1
    elif position_head in [(row - 2, col + 1), (row - 1, col + 2), (row - 2, col + 2)]:
        return row - 1, col + 1
    elif position_head in [(row + 2, col - 1), (row + 1, col - 2), (row + 2, col - 2)]:
        return row + 1, col - 1
    elif position_head in [(row + 2, col + 1), (row + 1, col + 2), (row + 2, col + 2)]:
        return row + 1, col + 1

    return position_tail


if __name__ == '__main__':
    with open('input.txt') as file:
        input: list[(str, int)] = list(map(parse_line, file.read().splitlines()))
        file.close()

    knots: list[tuple[int, int]] = [(0, 0) for _ in range(10)]
    positions_visited: list[set[tuple[int, int]]] = [set([]) for _ in range(10)]

    for [direction, amount] in input:
        for step in range(amount):
            knots[0] = move_head(direction, knots[0])
            for i, knot in enumerate(knots[1:]):
                knots[i + 1] = move_tail(knots[i], knots[i + 1])
                positions_visited[i + 1].add(knots[i + 1])

    print('Part one', len(positions_visited[1]))
    print('Part two', len(positions_visited[9]))
