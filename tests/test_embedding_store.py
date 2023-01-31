from random import randrange
from typing import List, Text

import numpy as np
import pytest

from embedding_store.base import VALID_COLUMN_ATTRIBUTE, EmbeddingStore


class MockEmbeddingStore(EmbeddingStore):
    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        return np.ones((len(sentences), 768))


@pytest.mark.unit
def test_retrieve_embeddings():
    query_sentences = ["I want some dinner", "Bella Chiao"]

    mock_embedding_store = MockEmbeddingStore()
    results = mock_embedding_store.retrieve_embeddings(query_sentences)

    assert results.shape == (2, 768)
    assert results[0].tolist() == np.ones(768).tolist()
    assert results[1].tolist() == np.ones(768).tolist()


@pytest.mark.unit
def test_retrieve_dataframe_embeddings():
    query_sentences = ["I want some dinner", "Bella Chiao"]

    mock_embedding_store = MockEmbeddingStore()
    results = mock_embedding_store.retrieve_dataframe_embeddings(query_sentences)

    assert results.shape == (2, 1)
    assert results[VALID_COLUMN_ATTRIBUTE].iloc[0].tolist() == np.ones(768).tolist()


@pytest.mark.integration
@pytest.mark.parametrize("embedding_store", ["jira_embedding_store"], indirect=True)
def test_retrieve_embeddings_from_external_source(embedding_store: EmbeddingStore):
    query_sentences = ["I want to listen the music.", "".join([str(randrange(0, 10)) for _ in range(10)]), "我要聽音樂"]

    results = embedding_store.retrieve_embeddings(sentences=query_sentences)
    assert results.shape[0] == 3

    results = embedding_store.retrieve_dataframe_embeddings(sentences=query_sentences)
    assert results.shape == (3, 1)
    assert not any(map(lambda x: x is None, results.index.to_list()))
    assert not any(map(lambda x: x is None, results[VALID_COLUMN_ATTRIBUTE].to_list()))
