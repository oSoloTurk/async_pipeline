from async_pipeline.structures import BasePipelineItem, PipelineItem
from async_pipeline.worker import ThreadWorker
from tests.utils.exception_tests import try_exception


def test_base_pipeline_item():
    """Base pipeline item test suite"""
    base_pipeline_item = BasePipelineItem(None)
    try_exception(NotImplementedError, base_pipeline_item.done)
    try_exception(NotImplementedError, base_pipeline_item.__call__)


def test_pipeline_item():
    """Pipeline item test suite"""

    def callback(item):
        """Callback"""
        pass

    pipeline_item = PipelineItem(None, callback)

    try_exception(AttributeError, pipeline_item)

    worker = ThreadWorker()
    worker.iterator.append(pipeline_item)

    def process(pipeline_item, item):
        """Process the item"""
        assert item is None
        pipeline_item.item = "test"

    worker.process = process

    worker.start()
    worker.stop()

    assert pipeline_item.item == "test"
