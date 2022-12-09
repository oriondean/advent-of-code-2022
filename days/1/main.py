from functools import reduce

def groupCalories(memo, value):
    print(memo)
    if value in ['', '\n']:
        return memo + [0]
    return memo[:-1] + [memo[len(memo) - 1] + int(value)]

if __name__ == '__main__':
    with open('input.txt') as file:
        result = reduce(groupCalories, file, [0])
        file.close()

    print('Part one', max(result))
    print('Part two', sum(sorted(result)[-3:]))


