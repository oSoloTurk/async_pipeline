from typing import Callable, Optional, Any


class BasePipelineItem:
    """
        This class is the base class for all pipeline items.
        It defines the interface for all pipeline items.
    """
    def __init__(self, item:Optional[Any], callback=Optional[Callable]):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError

    def done(self, *args: Any, **kwds: Any) -> Any:
        """
            This method is called when the pipeline item is done.
        """
        raise NotImplementedError
