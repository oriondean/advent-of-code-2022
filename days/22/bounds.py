def get_bounds(row: list[str]) -> (int, int):
    try:
        wall_min: int = row.index('#')
    except ValueError:
        wall_min: int = row.index('.')

    try:
        wall_max: int = list(reversed(row)).index('#')
    except ValueError:
        wall_max: int = list(reversed(row)).index('.')

    return (
        min(row.index('.'), wall_min),
        len(row) - min(list(reversed(row)).index('.'), wall_max) - 1
    )
