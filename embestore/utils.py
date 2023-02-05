from itertools import islice
from typing import Generator, Iterable


def chunks(x: Iterable, size: int) -> Generator:
    iterator = iter(x)
    chunk = list(islice(iterator, size))
    while chunk:
        yield chunk
        chunk = list(islice(iterator, size))
