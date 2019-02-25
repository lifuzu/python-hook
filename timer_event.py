#!python

import sched, time
from interface import implements
from event import Event


class TimerEvent(implements(Event)):

    def __init__(self, delay_ms: int = 10, priority: int = 1):
        self.name = "Timer"

        self.delay_ms = delay_ms
        self.priority = priority

        self.s = sched.scheduler(time.time, time.sleep)

    def name(self) -> str:
        return "Timer"

    # TODO: how to have fn return
    # def data(self) -> object:
    #     return {"a": 1, "b": 2}

    def emit(self) -> None:
        self.s.enter(self.delay_ms, self.priority, self.fn)
        self.s.run()

    def __call__(self, fn):

        def wrapper(*args, **kwargs):
            self.fn = fn
            self.emit()
        return wrapper


@TimerEvent(delay_ms = 5, priority = 1)
def a_function():
    print("in a_function")
    print(time.time())


if __name__ == "__main__":
    print(time.time())
    a_function()
