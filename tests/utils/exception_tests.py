def try_exception(excepted_exception, func, *args, **kwargs):
    """Try exception"""
    try:
        func(*args, **kwargs)
    except excepted_exception:
        pass
    else:
        raise AssertionError


async def try_exception_async(excepted_exception, func, *args, **kwargs):
    """Try exception"""
    try:
        await func(*args, **kwargs)
    except excepted_exception:
        pass
    else:
        raise AssertionError
