def find_start_of_message(chars, distinct_count):
    for i, char in enumerate(chars):
        if i < len(chars) - distinct_count:
            if len(set(chars[i: i + distinct_count])) == distinct_count:
                return i + distinct_count


if __name__ == '__main__':
    with open('input.txt') as file:
        input = file.readlines()[0]
        file.close()

    print('Part one', find_start_of_message(input, 4))
    print('Part two', find_start_of_message(input, 14))
