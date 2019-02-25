#!python

from interface import implements, Interface


class Event(Interface):

    # event name
    def name(self) -> str:
        pass

    # event data
    # def data(self) -> object:
    #     pass

    # event is emitted
    def emit(self) -> object:
        pass


