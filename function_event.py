#!python

from functools import wraps

class FunctionEvent(object):

    def __init__(self, fn):
        self.fn = fn
        self.funcs = set()

    def name(self) -> str:
        return "Function"

    # def data(self) -> object:
    #     return {"a": 1, "b": 2}

    def emit(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: run twice?
            return func(*args, **kwargs)

        if callable(func):
            self.funcs.add(func)

        return wrapper


    def __call__(self, *args, **kwargs):

        self.fn(*args, **kwargs)

        # processing the funcs
        for func in self.funcs:
            func()

@FunctionEvent
def a_function():
    print("in a_function")
    pass

@a_function.emit
def a_hook_func(a = 1, b = { "c" : 1}):
    print("in a_hook_func: {}".format(a))
    pass


if __name__ == "__main__":
    a_function()