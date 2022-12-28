from copy import copy


def sum_coordinates(result: list[(int, int)]) -> int:
    index_zero = result.index([q for q in result if q[0] == 0][0])
    length = len(result)
    return sum([result[(index_zero + value) % length][0] for value in range(1000, 4000, 1000)])


def mix(source: list[(int, int)], input: list[int]) -> list[(int, int)]:
    numbers: list[(int, int)] = copy(source)

    for i, number in enumerate(input):
        index = numbers.index([q for q in numbers if q[1] == i][0])
        popped = numbers.pop(index)
        numbers.insert((index + number) % len(numbers), popped)

    return numbers


if __name__ == '__main__':
    with open('input.txt') as file:
        input = list(map(int, file.read().splitlines()))
    file.close()

    result = mix([(x, i) for i, x in enumerate(input)], input)
    print('Part one', sum_coordinates(result))

    input_decrypted = [i * 811_589_153 for i in input]
    result = [(x, i) for i, x in enumerate(input_decrypted)]
    for x in range(0, 10):
        result = mix(result, input_decrypted)
    print('Part two', sum_coordinates(result))
