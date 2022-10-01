from typing import Any, Iterable, Optional

from async_pipeline.iterator import ConsumableQueueIterator


class BaseBucket:
    """
    This class is the base class for all buckets.
    It defines the interface for all buckets.
    """

    def __init__(self, bucket_name: str):
        pass

    def __iter__(self) -> Iterable:
        raise NotImplementedError

    def __getattr__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class Bucket(BaseBucket):
    """
    Bucket is a bucket that can be processed by a worker.
    """

    def __init__(self, bucket_name: str):
        super().__init__(bucket_name)
        self.bucket_name = bucket_name
        self.items = []

    def __iter__(self):
        return self.items.__iter__()

    def __getattr__(self, *args: Any, **kwds: Any) -> Any:
        return getattr(self.items, *args, **kwds)

    def __len__(self) -> int:
        return len(self.items)


class ConsumableBucket(BaseBucket):
    """
    ConsumableBucket is a bucket that can be processed by a worker.
    """

    def __init__(self, bucket_name: str):
        super().__init__(bucket_name)
        self.bucket_name = bucket_name
        self.items = ConsumableQueueIterator()

    def __iter__(self):
        return self.items.__iter__()

    def __getattr__(self, *args: Any, **kwds: Any) -> Any:
        return getattr(self.items, *args, **kwds)

    def __len__(self) -> int:
        return len(self.items)


class BaseStorage:
    """
    This class is the base class for all storages.
    It defines the interface for all storages.
    """

    def get(self, bucket_name: str = "default", **kwds: Any) -> Any:
        """
        Get item from the storage
        """
        raise NotImplementedError

    def put(self, bucket_name: str = "default", **kwds: Any) -> Any:
        """
        Put item to the storage
        """
        raise NotImplementedError

    def append(
        self, bucket_name: str = "default", item: Any = None, **kwds: Any
    ) -> Any:
        """
        Append item to the storage
        """
        raise NotImplementedError

    def __getitem__(self, item) -> Any:
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def items(self):
        """
        Return all items in the storage
        """
        raise NotImplementedError


class MultipleBucketStorage(BaseStorage):
    """
    MultipleBucketStorage is a storage that can be processed by a worker.
    """

    def __init__(self):
        self.buckets = {}

    def get(self, bucket_name: str = "default", **kwds: Any) -> Bucket:
        """
        Get item from the storage
        """
        if bucket_name not in self.buckets:
            self.buckets[bucket_name] = Bucket(bucket_name)
        return self.buckets[bucket_name]

    def put(
        self,
        bucket_name: str = "default",
        bucket: Optional[BaseBucket] = None,
        **kwds: Any
    ) -> Bucket:
        """
        Put item to the storage
        """
        if bucket_name not in self.buckets:
            self.buckets[bucket_name] = bucket
        return self.buckets[bucket_name]

    def append(
        self, bucket_name: str = "default", item: Optional[Any] = None, **kwds: Any
    ) -> Any:
        bucket = self.get(bucket_name)
        bucket.append(item)

    def __getitem__(self, item) -> Any:
        return self.get(item)

    def __iter__(self):
        return iter(self.buckets)

    def __len__(self):
        return len(self.buckets)

    def items(self):
        return self.buckets.items()
