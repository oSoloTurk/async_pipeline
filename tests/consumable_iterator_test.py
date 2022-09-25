from async_pipeline.iterator import ConsumableIterator, BaseIterator

def test_consumable_iterator():
    """Consumable iterator test suite"""
    items = ['a', 'b', 'c', 'd', 'e']
    iterator = ConsumableIterator(items, exits_if_empty=True)
    for item in iterator:
        assert item in items
    assert len(items) != len(iterator)
    iterator.append('f')
    assert len(iterator) == 1

def test_consumable_iterator_infinity():
    """Consumable iterator test suite"""
    items = ['a', 'b', 'c', 'd', 'e']
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
    
    def try_exception(excepted_exception, func, *args, **kwargs):
        """Try exception"""
        try:
            func(*args, **kwargs)
        except excepted_exception:
            pass
        else:
            raise AssertionError

    not_implemented_iterator = BaseIterator()
    try_exception(NotImplementedError, not_implemented_iterator.__iter__)
    try_exception(NotImplementedError, not_implemented_iterator.append, 1)
