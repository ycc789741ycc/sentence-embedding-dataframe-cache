from random import randrange
from typing import List, Text

import numpy as np
import pytest

from embestore.base import VALID_COLUMN_ATTRIBUTE, EmbeddingStore


class MockEmbeddingStore(EmbeddingStore):
    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        return np.ones((len(sentences), 768))


@pytest.mark.unit
def test_retrieve_embeddings():
    query_sentences = ["I want some dinner", "Bella Chiao"]

    mock_embestore = MockEmbeddingStore()
    results = mock_embestore.retrieve_embeddings(query_sentences)

    assert results.shape == (2, 768)
    assert results[0].tolist() == np.ones(768).tolist()
    assert results[1].tolist() == np.ones(768).tolist()


@pytest.mark.unit
def test_retrieve_dataframe_embeddings():
    query_sentences = ["I want some dinner", "Bella Chiao"]

    mock_embestore = MockEmbeddingStore()
    results = mock_embestore.retrieve_dataframe_embeddings(query_sentences)

    assert results.shape == (2, 1)
    assert results[VALID_COLUMN_ATTRIBUTE].iloc[0].tolist() == np.ones(768).tolist()


@pytest.mark.integration
@pytest.mark.parametrize("embestore", ["jira_embestore", "torch_embestore"], indirect=True)
def test_retrieve_embeddings_from_external_source(embestore: EmbeddingStore):
    query_sentences = ["I want to listen the music.", "".join([str(randrange(0, 10)) for _ in range(10)]), "我要聽音樂"]

    results = embestore.retrieve_embeddings(sentences=query_sentences)
    assert results.shape[0] == 3

    results = embestore.retrieve_dataframe_embeddings(sentences=query_sentences)
    assert results.shape == (3, 1)
    assert not any(map(lambda x: x is None, results.index.to_list()))
    assert not any(map(lambda x: x is None, results[VALID_COLUMN_ATTRIBUTE].to_list()))
