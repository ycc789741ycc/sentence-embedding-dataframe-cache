import pytest

from embestore.utils import chunks


@pytest.mark.unit
def test_chunks():
    arr = list(range(4))
    for chunk in chunks(arr, size=2):
        assert len(chunk) == 2
