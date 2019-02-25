
class condition(object):

    def __init__(self, fn):
        self.fn = fn
        self.retval = None

    def __call__(self):
         self.retval = self.fn()
         return self.retval

    @classmethod
    def equal(cls, val: any) -> bool:
        def decorator(function):
            def wrapper(*args, **kwargs):
                if val == True:
                    retval = function(*args, **kwargs)
                else:
                    retval = None
                return retval
            return wrapper
        return decorator


def compare_func(a, b):
    return a == b

@condition.equal(compare_func(1, 1))
def a_function():
    print("hello compare_func")

@condition.equal(True)
def a_true_function():
    print("hello True")

if __name__ == "__main__":
    a_function()
    a_true_function()