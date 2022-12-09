from functools import reduce

if __name__ == '__main__':
    with open('input.txt') as file:
        strategy: list[[str, str]] = reduce(lambda memo, value: memo + [value.split(' ')], file.read().splitlines(), [])
        file.close()

    typeScoreMap: dict[str, int] = {'X': 1, 'Y': 2, 'Z': 3}
    compareScoreMap: dict[str, int] = {
        'AX': 3, 'AY': 6, 'AZ': 0,
        'BX': 0, 'BY': 3, 'BZ': 6,
        'CX': 6, 'CY': 0, 'CZ': 3,
    }
    resultScoreMap: dict[str, int] = {'X': 0, 'Y': 3, 'Z': 6}
    findResultMap: dict[str, dict[str, str]] = {
        'X': {'A': 'Z', 'B': 'X', 'C': 'Y'},
        'Y': {'A': 'X', 'B': 'Y', 'C': 'Z'},
        'Z': {'A': 'Y', 'B': 'Z', 'C': 'X'}
    }

    print('Part one',
          reduce(lambda memo, value: memo + typeScoreMap[value[1]] + compareScoreMap[value[0] + value[1]], strategy, 0))
    print('Part one',
          reduce(lambda memo, value: memo + typeScoreMap[findResultMap[value[1]][value[0]]] + resultScoreMap[value[1]],
                 strategy, 0))
