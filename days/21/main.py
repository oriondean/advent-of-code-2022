from copy import copy


def run_operation(left: int, operator: str, right: int) -> int:
    return left + right if operator == '+' else left - right if operator == '-'\
        else left * right if operator == '*' else left // right


def compute_nodes(nodes: list[(str, str, str, str)], values: dict[str, int]) -> dict[str, int]:
    computed: dict[str, int] = copy(values)
    to_compute = copy(nodes)

    while len(to_compute):
        for monkey in to_compute:
            if monkey[1] in computed and monkey[3] in computed:
                computed[monkey[0]] = run_operation(computed[monkey[1]], monkey[2], computed[monkey[3]])
                to_compute.remove(monkey)

    return computed


def find_path(source: str, target: str) -> list[(int, int, int, int)]:
    current: str = source
    path: list[(int, int, int, int)] = [(current, 0)]

    while current != target:
        ancestor = [node for node in monkeys if node[1] == current or node[3] == current][0]
        path.insert(0, ancestor)
        current = ancestor[0]

    return path


def calculate_equalling_total(paths: list[(int, int, int, int)], values: dict[str, int]) -> int:
    value: int = 0

    for i, step in enumerate(paths[0:-1]):
        next_step = paths[i + 1][0]
        val = values[step[3 if step[1] == next_step else 1]]

        if step[0] == 'root':
            value = val
        elif step[2] == '+':
            value = value - val
        elif step[2] == '-':
            value = value + val if step[1] == next_step else (value - val) * -1
        elif step[2] == '*':
            value = value // val
        elif step[2] == '/':
            value = value * val if step[1] == next_step else (value // val) * -1

    return value


if __name__ == '__main__':
    values: dict[str, int] = dict()
    monkeys: list[(str, str, str, str)] = []

    with open('input.txt') as file:
        for line_raw in file:
            line = (line_raw.strip().split(': '))
            if line[1].isnumeric():
                values[line[0]] = int(line[1])
            else:
                monkeys.append((line[0], *line[1].split(' ')))
    file.close()

    values: dict[str, int] = compute_nodes(monkeys, values)
    print('Part one', values['root'])
    print('Part two', calculate_equalling_total(find_path('humn', 'root'), values))
