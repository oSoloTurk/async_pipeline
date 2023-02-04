from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from async_pipeline import storage as astorage
from async_pipeline.worker import BaseWorker


class PipelineStage:
    """
    A pipeline stage is a function that takes a single argument and
    returns a single value.
    """

    action: Callable
    worker: BaseWorker
    subscribe: Optional[List[Callable]] = None
    name: Optional[str] = None
    progress: bool = True

    def __init__(
        self,
        action: Callable,
        worker: BaseWorker,
        subscribe: Optional[List[Callable]] = None,
        name: Optional[str] = None,
        progress: bool = True,
    ):
        self.action = action
        self.worker = worker
        self.subscribe = subscribe
        self.name = name
        self.progress = progress

        if not isinstance(self.worker, BaseWorker):
            self.worker = self.worker()

    def start(self):
        self.worker.start()


@dataclass
class Pipeline:
    """
    A pipeline is a list of pipeline stages.
    """

    stages: List[PipelineStage]
    name: Optional[str] = None
    storage: Optional[astorage.BaseStorage] = None

    def start(self) -> None:
        """
        Start the pipeline
        """
        for stage in self.stages:
            stage.start()

    def add(self, bucket_name: str = "default", item: Any = None) -> None:
        """
        Add an item to the pipeline
        """
        if self.storage is None:
            raise Exception("No storage defined")
        self.storage.append(bucket_name, item)


def build_pipeline(
    stages: List[Union[PipelineStage, Dict]],
    name: Optional[str] = None,
    storage: Optional[astorage.BaseStorage] = None,
) -> Pipeline:
    """
    Build a pipeline from a list of pipeline stages.
    """
    if not storage:
        storage = astorage.MultipleBucketStorage()
    if not name:
        name = "default-pipeline"
    _stages = [
        PipelineStage(**stage) if isinstance(stage, dict) else stage
        for stage in stages
    ]
    return Pipeline(stages=_stages, name=name, storage=storage)
