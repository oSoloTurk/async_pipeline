import random
import time
from async_pipeline.pipeline import PipelineStage, build_pipeline
from async_pipeline.worker import ThreadWorker
from math import sqrt


def test_integrated_pipeline():
    NUMBER_COUNT = 10000000
    NUMBER_RANGE = 1000000

    numbers = []
    for _ in range(NUMBER_COUNT):
        numbers.append(random.randint(0, NUMBER_RANGE))

    output_sync = list(numbers)

    def do_sync():
        for index, number in enumerate(output_sync):
            output_sync[index] = number * number
        for index, number in enumerate(output_sync):
            output_sync[index] = number + number
        for index, number in enumerate(output_sync):
            output_sync[index] = sqrt(sqrt(number * number * number * number))

    sync_time = time.time()
    do_sync()
    sync_time = time.time() - sync_time

    stages = [
        {"action": lambda x: x * x, "worker": ThreadWorker},
        PipelineStage(
            action=lambda x: x + x,
            worker=ThreadWorker,
            subscribe=[print],
            name="test",
            progress=False,
        ),
        {
            "action": lambda x: sqrt(sqrt(x * x * x * x)),
            "worker": ThreadWorker,
        },
    ]

    async_time = time.time()

    pipeline = build_pipeline(stages=stages, name="test-pipeline")

    pipeline.start()

    async_time = time.time() - async_time

    assert (
        async_time > sync_time
    ), f"Async time {async_time} is not greater than sync time {sync_time}\n, estimated speedup: %{sync_time * 100 / async_time } (expected: > 1)"
