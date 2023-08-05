class TimeoutError(Exception):
    pass


class Timeout:
    def __init__(self, max_steps):
        self.max_steps = max_steps
        self.steps = 0

    def inc(self):
        self.steps += 1
        if self.steps >= self.max_steps:
            raise TimeoutError


class KarelSyntaxError(Exception):
    pass


class ExecutorSyntaxException(Exception):
    pass


class ExecutorRuntimeException(Exception):
    pass
