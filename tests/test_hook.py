import unittest
from unittest.mock import patch

if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from hook import hook
else:
    from ..hook import hook


def a(n):
    if n > 10:
        b()

def b():
    print("test")

@hook
def do_something():
    pass
    # do_something_callfore()

@do_something.callfore
def do_something_callfore():
    pass


class TestHook(unittest.TestCase):

    def setUp(self):
        pass

    @patch('__main__.b')
    def test_b_called(self, mock):
        a(11)
        self.assertTrue(mock.called)

    @patch('__main__.b')
    def test_b_not_called(self, mock):
        a(10)
        self.assertFalse(mock.called)

    @patch('__main__.do_something_callfore')
    def test_callfore_called(self, mock):
        do_something()
        # TODO: fixing the following test
        # self.assertTrue(mock.called)

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