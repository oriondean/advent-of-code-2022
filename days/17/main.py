def add_rock(map: list[str], rows: list[str]) -> None:
    for i, row in enumerate(reversed(rows)):
        rock_start = 2 + row.index('#')
        rock_len = (2 + row.rindex('#')) - rock_start
        row = len(map) - len(rows) + i
        map[row] = map[row][0: rock_start] + ('@' * (rock_len + 1)) + map[row][rock_start + 1 + rock_len:]


def move_rock(map: list[str], pattern: str, row_rock: int, height: int) -> None:
    if pattern == '<':
        if all([lines.index('@') > 0 and '#@' not in lines for lines in map[row_rock:row_rock + height]]):
            for row in range(row_rock, row_rock + height):
                line: list[str] = list(map[row])
                line[map[row].index('@') - 1] = '@'
                line[map[row].rindex('@')] = '.'
                map[row] = ''.join(line)
    elif pattern == '>':
        if all([lines.rindex('@') < (len(lines) - 1) and '@#' not in lines for lines in map[row_rock:row_rock + height]]):
            for row in range(row_rock, row_rock + height):
                line: list[str] = list(map[row])
                line[map[row].index('@')] = '.'
                line[map[row].rindex('@') + 1] = '@'
                map[row] = ''.join(line)


def can_move_down(map: list[str], row: int, height: int) -> bool:
    for r in range(row, row + height):
        if '#' in map[r][map[r + 1].index('@'):map[r + 1].rindex('@') + 1]:
            return False
    return True


def move_rock_down(map: list[str], row: int, height: int) -> None:
    for row in range(row, row + height):
        rock_start, rock_end = map[row + 1].index('@'), map[row + 1].rindex('@')
        rock_len = rock_end - rock_start
        map[row + 1] = map[row + 1].replace('@', '.')
        map[row] = map[row][0: rock_start] + ('@' * (rock_len + 1)) + map[row][rock_start + 1 + rock_len:]


def set_rock_landed(map: list[str], row: int, height: int) -> None:
    for r in range(row, row + height):
        map[r] = map[r].replace('@', '#')


def resize_map(map: list[str], row: int, height: int, width_map: int) -> list[str]:
    if row + height > len(map):
        return map + ['.' * width_map for _ in range(row + height - len(map))]
    else:
        return map[0: row + height]


def run_simulation(duration: int, pattern_jet: str, types_rock: list[list[str]]) -> None:
    state: str = 'rock-landed'
    width_map = 7
    map: list[str] = ['.' * width_map for _ in range(1)]
    highest_rock_seen: int = 0
    row_rock: int = 0
    rock_height: int = 1
    rocks_landed: int = 0
    types_rock_index: int = -1
    pattern_jet_index: int = 0

    while rocks_landed < duration:
        if state == 'rock-landed':
            types_rock_index = (types_rock_index + 1) % len(types_rock)
            rock_height = len(types_rock[types_rock_index])

            if (cycle_start + cycle_length) < rocks_landed < (cycle_start + (cycle_length * 2)):
                cycle_diff.append(highest_rock_seen - (cycle_start_delta + cycle_increase))

            row_rock = highest_rock_seen + 3
            map = resize_map(map, row_rock, rock_height, width_map)
            add_rock(map, types_rock[types_rock_index])
            state = 'jet-firing'
        elif state == 'jet-firing':
            move_rock(map, pattern_jet[pattern_jet_index], row_rock, rock_height)
            pattern_jet_index = (pattern_jet_index + 1) % len(pattern_jet)
            state = 'rock-falling'
        elif state == 'rock-falling':
            if row_rock <= 0 or not can_move_down(map, row_rock - 1, rock_height):
                set_rock_landed(map, row_rock, rock_height)
                rocks_landed += 1
                if rocks_landed == 2023:
                    print('Part one', highest_rock_seen, highest_rock_seen == 3193)

                highest_rock_seen = max(row_rock + rock_height, highest_rock_seen)
                state = 'rock-landed'
            else:
                row_rock -= 1
                move_rock_down(map, row_rock, rock_height)
                state = 'jet-firing'


if __name__ == '__main__':
    with open('input.txt') as file:
        pattern_jet: str = file.read().splitlines()[0]
        file.close()

    types_rock: list[list[str]] = \
        [['####'], ['.#.', '###', '.#.'], ['..#', '..#', '###'], ['#', '#', '#', '#'], ['##', '##']]

    # These magic numbers gleamed from spotting a repeating cycle of rock type and jet pattern index
    cycle_start: int = 731
    cycle_start_delta: int = 1165
    cycle_increase: int = 2753
    cycle_length: int = 1745
    cycle_diff: list[int] = [0]

    run_simulation(3000, pattern_jet, types_rock)

    rocks_stopped = 1_000_000_000_000
    a = cycle_start_delta + (((rocks_stopped - cycle_start) // cycle_length) * cycle_increase) \
        + cycle_diff[(rocks_stopped - cycle_start) % cycle_length]
    print('Part two', rocks_stopped, a, a == 1577650429835)
