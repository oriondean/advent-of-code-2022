from typing import TextIO


def parse_input(file: TextIO) -> list[(int, int)]:
    elves: list[(int, int)] = []
    x: int = 0
    y: int = 0

    for line_raw in file:
        for character in line_raw.strip():
            if character == '#':
                elves.append((x, y))
            y += 1
        x += 1
        y = 0

    return elves


def has_adjacent_neighbour(positions: set[(int, int)], x: int, y: int) -> bool:
    return bool({(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                 (x + 1, y + 1)}.intersection(positions))


def get_proposed_positions(elves: list[(int, int)], positions_considered: list[list[(int, int)]]) -> list[(int, int)]:
    positions_proposed: list[(int, int)] = list()
    elves_set = set(elves)

    for elf in elves:
        if not has_adjacent_neighbour(elves_set, *elf):
            positions_proposed.append(elf)
        else:
            position_proposed = None
            for positions in positions_considered:
                if not set([(elf[0] + p[0], elf[1] + p[1]) for p in positions]).intersection(elves_set):
                    position_proposed = (elf[0] + positions[0][0], elf[1] + positions[0][1])
                    positions_proposed.append(position_proposed)
                    break
            if not position_proposed:
                positions_proposed.append(elf)

    return positions_proposed


def run_simulation(elves: list[(int, int)], is_part_one: bool) -> (list[(int, int)], int):
    positions_considered: list[list[(int, int)]] = [
        [(-1, 0), (-1, 1), (-1, -1)], [(1, 0), (1, 1), (1, -1)],
        [(0, -1), (-1, -1), (1, -1)], [(0, 1), (-1, 1), (1, 1)],
    ]
    turns: int = 0

    while turns < 10 if is_part_one else True:
        positions_proposed: list[(int, int)] = get_proposed_positions(elves, positions_considered)

        if positions_proposed == elves:
            return elves, turns + 1

        elves = [position if positions_proposed.count(position) == 1 else elves[index] for
                 index, position in enumerate(positions_proposed)]
        positions_considered = positions_considered[1:] + [positions_considered[0]]
        turns += 1

    return elves, turns


def count_empty_tiles(elves: list[(int, int)]) -> int:
    bounds_x: list[(int, int)] = sorted(elves, key=lambda elf: elf[0])
    bounds_y: list[(int, int)] = sorted(elves, key=lambda elf: elf[1])
    count: int = 0

    for x in range(bounds_x[0][0], bounds_x[-1][0] + 1):
        count += len([y for y in range(bounds_y[0][1], bounds_y[-1][1] + 1) if (x, y) not in elves])

    return count


if __name__ == '__main__':
    with open('input.txt') as file:
        elves: list[(int, int)] = parse_input(file)
        file.close()

    (elves_one, _) = run_simulation(elves, True)
    print('Part one', count_empty_tiles(elves_one))

    (_, turns2) = run_simulation(elves, False)
    print('Part two', turns2)
