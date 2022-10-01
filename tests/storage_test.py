from async_pipeline.storage import (
    BaseStorage,
    MultipleBucketStorage,
    BaseBucket,
    Bucket,
)
from tests.utils.exception_tests import try_exception, try_exception_async

import pytest

pytestmark = pytest.mark.asyncio


async def test_base_storage():
    """Base storage test suite"""
    base_storage = BaseStorage()
    try_exception(NotImplementedError, base_storage.get)
    try_exception(NotImplementedError, base_storage.put)
    try_exception(NotImplementedError, base_storage.append)
    try_exception(NotImplementedError, base_storage.__getitem__, 1)
    try_exception(NotImplementedError, base_storage.__iter__)
    try_exception(NotImplementedError, base_storage.__len__)
    try_exception(NotImplementedError, base_storage.items)


async def test_multiple_bucket_storage():
    """Multiple bucket storage test suite"""
    multiple_bucket_storage = MultipleBucketStorage()
    bucket_names = ["bucket1", "bucket2", "bucket3"]
    items = ["a", "b", "c"]
    for bucket_name, item in zip(bucket_names, items):
        multiple_bucket_storage.append(bucket_name, item)

    assert len(multiple_bucket_storage) == len(bucket_names)

    for bucket_name, bucket in multiple_bucket_storage.items():
        bucket.append("test")

    for bucket_name in multiple_bucket_storage:
        bucket = multiple_bucket_storage[bucket_name]
        assert len(bucket) == 2

    multiple_bucket_storage.put("bucket4", Bucket("bucket4"))
    assert len(multiple_bucket_storage) == len(bucket_names) + 1


def test_base_bucket():
    """Base bucket test suite"""
    base_bucket = BaseBucket(bucket_name="test")
    try_exception(NotImplementedError, base_bucket.__getattr__)
    try_exception(NotImplementedError, base_bucket.__len__)
