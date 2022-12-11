class Monkey:
    def __init__(self):
        self.items = []
        self.operation_raw = ''
        self.operation = None
        self.test_divisible_by = 1
        self.test_pass_target = 0
        self.test_fail_target = 0
        self.inspection_count = 0

    def inspect(self, item, modifier_worry):
        level_worry = self.operation(self.operation_raw, item)
        level_worry = modifier_worry(level_worry)

        is_pass = level_worry % self.test_divisible_by == 0
        target_throw = self.test_pass_target if is_pass else self.test_fail_target

        return target_throw, level_worry
