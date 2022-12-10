def draw_pixel(screen, index_pixel) -> None:
    (row, col) = index_pixel
    screen[row][col] = '#' if count_register in [col - 1, col, col + 1] else '.'


def move_position(index_pixel, width) -> (int, int):
    (row, col) = index_pixel

    if col == width:
        if row == width:
            return 0, 0
        else:
            return row + 1, 0

    return row, col + 1


if __name__ == '__main__':
    with open('input.txt') as file:
        input: list[str] = file.read().splitlines()
        file.close()

    width_screen: int = 39
    count_instruction_index: int = 0
    count_register: int = 1
    index_pixel: (int, int) = (0, 0)
    is_executing: bool = False
    history_cycles: list[int] = []
    screen: list[list[str]] = [['-' for __ in range(40)] for _ in range(40)]

    for i in range(0, 240):
        instruction: str = input[count_instruction_index]

        if instruction == 'noop':
            history_cycles.append(count_register)
            draw_pixel(screen, index_pixel)
            index_pixel = move_position(index_pixel, width_screen)
            count_instruction_index += 1
        elif instruction.startswith('addx'):
            value = int(instruction.split(' ')[1])
            draw_pixel(screen, index_pixel)
            index_pixel = move_position(index_pixel, width_screen)

            if is_executing:
                count_register += value
                count_instruction_index += 1
            is_executing = not is_executing

            history_cycles.append(count_register)

    print('Part one', sum(map(lambda value: history_cycles[value - 2] * value, [20, 60, 100, 140, 180, 220])))

    print('Part two')
    for r in range(0, 6):
        print(''.join(screen[r]))
