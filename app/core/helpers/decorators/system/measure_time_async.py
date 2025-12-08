import time
import functools
from typing import Callable, Any

from core.logger.logger import Logger
from core.logger.messages.measure_time import MeasureFuncTimeMessage

logger = Logger


def measure_time_async(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args: tuple, **kwargs: dict) -> Any:
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(MeasureFuncTimeMessage(name=func.__name__, time=end - start))
        return result

    return wrapper
