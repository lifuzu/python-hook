import unittest
from unittest.mock import Mock
from unittest.mock import patch

if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from hook import hook
else:
    from hook import hook


# def a(n):
#     if n > 10:
#         b()

# def b():
#     print("test")

# @hook
# def do_something():
#     pass

# @do_something.callfore
# def do_something_callfore():
#     return("do_something_callfore")


# func = do_something
# callfore_func = do_something_callfore
# print(func.callfores)

# do_something()

# print(dir(func.callfores[0]))
# print(func.callfores[0].__module__)
# print(func.callfores[0].__name__)
# print(func.callfores[0].__qualname__)
# print(callfore_func)
# print(getattr(hook(do_something()), 'callfores'))

class TestPythonHook(unittest.TestCase):

    def setUp(self):
        pass

    # @patch('__main__.b')
    # def test_b_called(self, mock):
    #     a(11)
    #     self.assertTrue(mock.called)

    # @patch('__main__.b')
    # def test_b_not_called(self, mock):
    #     a(10)
    #     self.assertFalse(mock.called)

    def test_callfore(self):

        @hook
        def do_something():
            pass

        @do_something.callfore
        def a_callfore():
            pass

        callfores = [func.__module__ + '.' + func.__name__ for func in do_something.callfores]

        self.assertTrue(len(callfores) == 1)
        self.assertTrue(a_callfore.output in callfores)

    def test_callback(self):

        @hook
        def do_something():
            pass

        @do_something.callback
        def a_callback():
            pass

        callbacks = [func.__module__ + '.' + func.__name__ for func in do_something.callbacks]

        self.assertTrue(len(callbacks) == 1)
        self.assertTrue(a_callback.output in callbacks)

    def test_callfore_called(self):

        @hook
        def do_something():
            pass

        @do_something.callfore
        def a_callfore():
            return {"a": 1}

        @do_something.callfore
        def a_callfore_without_return():
            pass

        do_something()

        self.assertFalse(do_something.output in do_something.outputs)

        self.assertEqual(do_something.outputs[a_callfore.output], {"a": 1})
        self.assertNotEqual(do_something.outputs[a_callfore.output], {"b": 2})

        self.assertTrue(len(do_something.outputs) == 1)
        self.assertFalse(a_callfore_without_return.output in do_something.outputs)

    def test_callback_called(self):

        @hook
        def do_something():
            return {"a": 1}

        @do_something.callback
        def a_callback():
            return {"b": 2}

        @do_something.callback
        def a_callback_without_return():
            pass

        do_something()

        self.assertTrue(len(do_something.outputs) == 2)
        self.assertTrue(do_something.output in do_something.outputs)

        self.assertEqual(do_something.outputs[do_something.output], {"a": 1})

        self.assertEqual(do_something.outputs[a_callback.output], {"b": 2})
        self.assertNotEqual(do_something.outputs[a_callback.output], {"a": 1})

        self.assertFalse(a_callback_without_return.output in do_something.outputs)

    # @patch('__main__.do_something')
    # @patch('__main__.do_something_callfore')
    # def test_callfore_called(self, mock, mock2):
    #     func = mock()
    #     print(dir(func))
    #     # self.assertEqual(mock2.output, "do_something_callfore")
    #     self.assertTrue(func.called)

    # @patch('__main__.' + func.callfores[0].__name__)
    # def test_callfore_called(self, mock):
    #     # func = Mock()
    #     # decorated_func = do_something.callfore(mock)
    #     # retval = decorated_func()
    #     print(do_something())
    #     # print(dir(hook))
    #     # print(func.callfores)
    #     # assert mock.assert_called_once()
    #     # self.assertEqual(mock.return_value, "do_something_callfore")
    #     # assert mock.called
    #     # TODO: fixing the following test
    #     self.assertTrue(mock.called)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()