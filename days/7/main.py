from functools import reduce

from anytree import Node, PostOrderIter


def directory_change(command, directory_current) -> Node:
    directory_name = command.split(' ')[-1]

    if directory_name == '..':
        return directory_current.parent
    else:
        return [x for x in directory_current.children if x.name == directory_name][0]


def run_command(command, directory_current) -> Node:
    if command == '$ cd /':
        return directory_root
    elif command.startswith('$ cd '):
        return directory_change(command, directory_current)
    elif command.startswith('dir'):
        Node(command.split(' ')[-1], directory_current, file_size=0)
    elif command == '$ ls':
        return directory_current  # no-op
    else:
        file_size = int(command.split(' ')[0])
        directory_current.file_size += file_size
        for ancestor in directory_current.ancestors:
            ancestor.file_size += file_size

    return directory_current


def calculate_file_sizes() -> None:
    for node in PostOrderIter(directory_root):
        node.file_size = sum(map(lambda file: file[1], node.files)) + (
            0 if node.is_leaf else sum(map(lambda child: child.file_size, node.children)))


if __name__ == '__main__':
    directory_root = Node('/', file_size=0)
    directory_current = directory_root

    with open('input.txt') as file:
        for line in file:
            directory_current = run_command(line.strip(), directory_current)

    print('Part one', sum([x.file_size for x in PostOrderIter(directory_root) if x.file_size <= 100_000]))

    space_total: int = 70_000_000
    space_needed: int = 30_000_000
    space_to_delete: int = space_needed - (space_total - directory_root.file_size)

    print('Part two', reduce(lambda memo, node: node.file_size if space_to_delete < node.file_size < memo else memo,
                             PostOrderIter(directory_root), space_needed))
