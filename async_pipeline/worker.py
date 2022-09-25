from abc import abstractmethod
from threading import Thread
from typing import Any, Optional
from async_pipeline.iterator import ConsumableIterator


class BaseWorker:
    """
    This class is the base class for all workers.
    It defines the interface for all workers.

    self.status = 'idle' for default
    """

    def __init__(self):
        self._status: str = "idle"

    @property
    def status(self):
        """
        Get the status of the worker
        """
        return self._status

    @abstractmethod
    def pause(self):
        """Pause the worker"""
        raise NotImplementedError

    @abstractmethod
    def resume(self):
        """Resume the worker"""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop the worker"""
        raise NotImplementedError

    @abstractmethod
    def start(self):
        """Start the worker"""
        raise NotImplementedError


class ThreadWorker(BaseWorker):
    """
    ThreadWorker is a worker that runs in a thread.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iterator: ConsumableIterator = ConsumableIterator(
            items=kwargs.get("items", []), exits_if_empty=False
        )
        self._thread: Optional[Thread] = None

    @abstractmethod
    def process(self, pipeline_item, item):
        """
        This method is called by the worker to process the item.
        This method should be implemented by the child class.
        """
        raise NotImplementedError

    def _run(self):
        for pipeline_item in self.iterator:
            if self.status in ("stopped", "idle"):
                break
            if pipeline_item is None:
                continue
            response: Optional[Any] = self.process(pipeline_item, pipeline_item.item)
            pipeline_item.done(response)

    def pause(self):
        """
        Pause the worker
        Workers listen to the status of the worker for pause and resume.
        """
        if self.status == "running":
            self._status = "paused"
        else:
            raise Exception("Worker is not running")

    def resume(self):
        """
        Pause the worker
        Workers listen to the status of the worker for pause and resume.
        """
        if self.status == "paused":
            self._status = "running"
        else:
            raise Exception("Worker is not paused")

    def stop(self):
        """Stop the worker"""
        if self.status == "running":
            self._status = "stopped"
            self._stop()
        else:
            raise Exception("Worker is not running")

    def start(self):
        """Start the worker"""
        if self.status == "idle":
            self._status = "running"
            self._start()
        else:
            raise Exception("Worker is not idle")

    def _start(self):
        self._thread = Thread(target=self._run)
        self._thread.start()

    def _stop(self):
        self._thread.join()
        self._thread = None
