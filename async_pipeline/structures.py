from asyncio import Queue
from typing import Any, Callable, Optional


class BasePipelineItem:
    """
    This class is the base class for all pipeline items.
    It defines the interface for all pipeline items.
    """

    def __init__(self, item: Optional[Any], callback=Optional[Callable]):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError

    def done(self, *args: Any, **kwds: Any) -> Any:
        """
        This method is called when the pipeline item is done.
        """
        raise NotImplementedError


class PipelineItem(BasePipelineItem):
    """
    PipelineItem is a pipeline item that can be processed by a worker.
    """

    def __init__(self, item: Optional[Any], callback: Optional[Callable] = None):
        super().__init__(item, callback)

        self.item = item
        self.callback = callback

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.item.__call__(*args, **kwds)

    def done(self, *args: Any, **kwds: Any) -> Any:
        if self.callback:
            self.callback(*args, **kwds)
