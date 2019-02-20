
from functools import wraps

class delegate(object):
    """docstring for delegate"""
    def __init__(self, func):
        self.callfores = []
        self.callbacks = []
        self.func = func
        self.outputs = {}

    def callfore(self, func):

        def wrapper(*args, **kwargs):
            print("In callfore wrapper: {}".format(args))
            for k, v in kwargs.items():
                print("{k} = {v}".format(k, v))
            return func(*args, **kwargs)

        if callable(func):
            self.callfores.append(func)

        return wrapper

    def callback(self, func, args: dict = None):

        def wrapper(*args, **kwargs):
            print("In callfore wrapper: {}".format(args))
            for k, v in kwargs.items():
                print("{k} = {v}".format(k, v))
            return func(*args, **kwargs)

        if callable(func):
            self.callbacks.append(func)

        return wrapper

    def inject_vars(self, *ext_args, **ext_kwargs):
        """"Decorator factory"""
        argv = vars()
        def vars_injector(func):
            @wraps(func)
            def decorator(*args, **kwargs):
                try:
                    func_globals = func.__globals__     # Python 2.6+
                except AttributeError:
                    func_globals = func.func_globals    # Earlier versions

                saved_values = func_globals.copy()      # Shallow copy of dict

                # print(', '.join(['{}={!r}'.format(k, v) for k, v in ext_kwargs.items()]))
                if ext_args:
                    context = ext_args[0]
                elif argv['ext_kwargs']:
                    context = argv['ext_kwargs']
                else:
                    context = {}

                if isinstance(context, dict):
                    for k, v in context.items():
                        if isinstance(v, dict):
                            context[k] = v
                        elif v in self.outputs:
                            context[k] = self.outputs[v]
                        else:
                            raise Exception(f"ERROR: check if the function: {v} return dict!".format(v))
                if context:
                    func_globals.update(context)

                try:
                    result = func(*args, **kwargs)
                finally:
                    func_globals = saved_values         # Restore the changes

                return result
            return decorator
        return vars_injector

    def __call__(self, *args, **kwargs):
        # processing the funcs in callfores
        for func in self.callfores:
            # print('call in {}'.format(func))
            retval = func()

            if retval is not None:
                self.outputs[func.__qualname__] = retval

        # processing the base func
        retval = self.func(*args, **kwargs)

        if retval is not None:
            self.outputs[self.func.__qualname__] = retval

        # processing the funcs in callbacks
        for func in self.callbacks:
            retval = func()

            if retval is not None:
                self.outputs[func.__qualname__] = retval

@delegate
def do_something(a: int = 5, b: int = 4):
    print("do something: {}, {}".format(a, b))
    return {'a': a, 'b': b}


@do_something.callfore
def do_something_before_1(any: int = 3):
    print("do do_something_before_1: {}".format(any))
    return {'a': 12 + any, 'z': 34}

@do_something.callfore
@do_something.inject_vars({'retval': 'do_something_before_1'})
# @do_something.inject_vars(retval = 'do_something_before_1')
# @do_something.inject_vars({'retval': {'a': 12, 'z': 34}})
def do_something_before_2(other = "helo other"):
    print("do do_something_before_2: {}".format(other))
    print("a: ", retval['a'])
    return {'a': 12 + retval['a'], 'z': 34}


@do_something.callback
@do_something.inject_vars(retval = 'do_something_before_2', retval2 = 'do_something')
def do_something_after_1(any: int = 888):
    print("do do_something_after_1: {}".format(any))
    print("a in do_something_after_1: {}".format(any + retval['a'] + retval2['b']))
    print("retval: {}".format(retval))
    print("retval_2: {}".format(retval2))
    return {}

@do_something.callback
@do_something.inject_vars(retval = 'do_something_after_1')
def do_something_after_2(other_dict = {"a": 12, "b": 34}):
    print("do do_something_after_2: {}".format(other_dict))



if __name__ == "__main__":
    do_something(6, 7)