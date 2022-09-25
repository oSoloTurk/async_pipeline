from async_pipeline.iterator import (
    ConsumableIterator,
    BaseIterator,
    ConsumableQueueIterator,
)
from tests.utils.exception_tests import try_exception


def test_consumable_iterator():
    """Consumable iterator test suite"""
    items = ["a", "b", "c", "d", "e"]
    iterator = ConsumableIterator(items, exits_if_empty=True)
    for item in iterator:
        assert item in items
    assert len(items) != len(iterator)
    iterator.append("f")
    assert len(iterator) == 1


def test_consumable_iterator_infinity():
    """Consumable iterator test suite"""
    items = ["a", "b", "c", "d", "e"]
    iterator = ConsumableIterator(items, exits_if_empty=False)
    items.append(None)
    for item in iterator:
        assert item in items
        items.remove(item)
        if len(items) == 0:
            break
    assert len(items) == len(iterator)
    iterator.append(6)
    assert len(iterator) == 1


def test_consumable_iterator_source():
    """Consumable iterator test suite"""

    not_implemented_iterator = BaseIterator()
    try_exception(NotImplementedError, not_implemented_iterator.__iter__)
    try_exception(NotImplementedError, not_implemented_iterator.append, 1)


def test_consumable_queue_iterator():
    """Consumable queue iterator test suite"""
    iterator = ConsumableQueueIterator(exits_if_empty=True)
    items = ["a", "b", "c", "d", "e"]
    for item in items:
        iterator.append(item)

    assert len(iterator) == len(items)

    for item in iterator:
        assert item in items
    assert len(items) != len(iterator)
    iterator.append("f")
    assert len(iterator) == 1
