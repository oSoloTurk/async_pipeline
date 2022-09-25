from async_pipeline.worker import BaseWorker
from tests.utils.exception_tests import try_exception

def test_base_worker():
    """Base worker test suite"""
    base_worker = BaseWorker()
    try_exception(NotImplementedError, base_worker.pause)
    try_exception(NotImplementedError, base_worker.resume)
    try_exception(NotImplementedError, base_worker.stop)
    try_exception(NotImplementedError, base_worker.start)
    assert base_worker.status == 'idle'
