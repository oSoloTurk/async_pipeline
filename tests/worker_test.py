from async_pipeline.structures import PipelineItem
from async_pipeline.worker import BaseWorker, ThreadWorker
from tests.utils.exception_tests import try_exception


def test_base_worker():
    """Base worker test suite"""
    base_worker = BaseWorker()
    try_exception(NotImplementedError, base_worker.pause)
    try_exception(NotImplementedError, base_worker.resume)
    try_exception(NotImplementedError, base_worker.stop)
    try_exception(NotImplementedError, base_worker.start)
    assert base_worker.status == "idle"


def test_thread_worker():
    """Thread worker test suite"""
    thread_worker = ThreadWorker()
    try_exception(NotImplementedError, thread_worker.process, None, None)
    assert thread_worker.status == "idle"

    item = PipelineItem("test")
    thread_worker.iterator.append(item)

    def process(pipeline_item, item):
        """Process the item"""
        assert item == "test"
        pipeline_item.item = "test2"

    thread_worker.process = process

    thread_worker.start()
    try_exception(Exception, thread_worker.start)
    assert thread_worker.status == "running"

    thread_worker.pause()
    try_exception(Exception, thread_worker.pause)
    assert thread_worker.status == "paused"

    thread_worker.resume()
    try_exception(Exception, thread_worker.resume)
    assert thread_worker.status == "running"

    thread_worker.stop()
    try_exception(Exception, thread_worker.stop)
    assert thread_worker.status == "stopped"

    assert item.item == "test2"
