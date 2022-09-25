from abc import abstractmethod


class BaseWorker:
    """
        This class is the base class for all workers.
        It defines the interface for all workers.

        self.status = 'idle' for default
    """
    def __init__(self, *args, **kwargs):
        self._status = 'idle'

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