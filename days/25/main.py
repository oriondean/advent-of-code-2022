def to_decimal(snafu: str) -> int:
    value: int = 0
    chars: list[str] = list(snafu)
    modifier_minus: int = 0

    for i, c in enumerate(reversed(chars)):
        if c.isalnum():
            value += ((5 ** i) * int(c)) - modifier_minus
            modifier_minus = 0
        elif c in ['-', '=']:
            modifier_minus += (5 ** i) * (1 if c == '-' else 2)

    return value


def get_required_digits(decimal: int) -> int:
    digits_required: int = 1
    limit: int = 2

    while decimal > limit:
        limit += ((5 ** digits_required) * 2)
        digits_required += 1

    return digits_required


def to_snafu(decimal: int) -> str:
    chars: list[str] = ['=', '-', '0', '1', '2']
    digits_required: int = get_required_digits(decimal)
    result: str = '2' * digits_required

    for i in range(0, digits_required):
        result = result[:i] + '2' + (len(result[i + 1:]) * '=')
        while to_decimal(result) > decimal:
            result = result[:i] + chars[chars.index(result[i]) - 1] + (len(result[i + 1:]) * '=')

    return result


if __name__ == '__main__':
    with open('input.txt') as file:
        input = file.read().splitlines()
        file.close()

    print('Result', to_snafu(sum([to_decimal(value) for value in input])))
