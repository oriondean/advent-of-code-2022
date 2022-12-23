from queue import SimpleQueue


def get_edges(x: int, y: int, z: int) -> set[(int, int, int)]:
    return {(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)}


def get_neighbour_count(cubes: set[(int, int, int)], position: (int, int, int)) -> int:
    return len(get_edges(*position).intersection(cubes))


def is_outside(x: int, y: int, z: int, s_x: int, s_y: int, s_z: int, e_x: int, e_y: int, e_z: int) -> bool:
    return x < s_x - 1 or x > e_x + 1 or y < s_y - 1 or y > e_y + 1 or z < s_z - 1 or z > e_z + 1


def breadth_first_search_lava(cubes: set[(int, int, int)], start: (int, int, int), end) -> set[int]:
    queue: SimpleQueue[(int, int, int)] = SimpleQueue()
    queue.put(start)
    visited: set[(int, int, int)] = set(start)

    while not queue.empty():
        (x, y, z) = queue.get()

        if (x, y, z) == end:
            return visited

        for position in get_edges(x, y, z):
            if position not in visited and position not in cubes and not is_outside(*position, *start, *end):
                visited.add(position)
                queue.put(position)

    return visited


if __name__ == '__main__':
    with open('input.txt') as file:
        cubes = set([tuple(map(int, line.split(','))) for line in file.read().splitlines()])
    file.close()

    range_x: list[int] = sorted([point[0] for point in cubes])
    range_y: list[int] = sorted([point[1] for point in cubes])
    range_z: list[int] = sorted([point[2] for point in cubes])
    start: tuple[int, int, int] = (range_x[0], range_y[0], range_z[0])
    end: tuple[int, int, int] = (range_x[-1], range_y[-1], range_z[-1])
    seen: set[(int, int, int)] = breadth_first_search_lava(cubes, start, end)

    print('Part one', sum([6 - get_neighbour_count(cubes, cube) for cube in cubes]))
    print('Part two', sum([len([edge for edge in get_edges(*position) if edge in seen]) for position in cubes]))
