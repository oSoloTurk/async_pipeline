"""Module using for more readabilty"""
from asyncio import Queue, QueueEmpty
from typing import Iterable


class BaseIterator(Iterable):
    """Base class for iterators"""

    def __iter__(self):
        raise NotImplementedError

    def append(self, item):
        """Append item to the iterator"""
        raise NotImplementedError


class ConsumableIterator(BaseIterator):
    """
    ConsumableIterator is a generator that can be consumed iterated items
    """

    def __init__(self, items: list, exits_if_empty: bool = True):
        self.items = list(items)  # Take clone of the list
        self.exits_if_empty = exits_if_empty

    def __iter__(self):
        _item = None  # Item to return
        while True:
            try:
                _item = self.items.pop()
            except IndexError:
                _item = None
            finally:
                yield _item
            if not self.items and self.exits_if_empty:
                break

    def __len__(self):
        return len(self.items)

    def append(self, item):
        """Append item to the end of the list"""
        self.items.append(item)


class ConsumableQueueIterator(ConsumableIterator):
    """
    ConsumableQueueIterator is a generator that can be consumed iterated items
    """

    def __init__(self, exits_if_empty: bool = True):
        super().__init__(items=[], exits_if_empty=exits_if_empty)
        self.items = Queue()

    def __iter__(self):
        _item = None  # Item to return
        while True:
            try:
                _item = self.items.get_nowait()
            except QueueEmpty:
                _item = None
                if self.exits_if_empty:
                    break
            yield _item

    def __len__(self):
        return self.items.qsize()

    def append(self, item):
        """Append item to the end of the list"""
        self.items.put_nowait(item)
