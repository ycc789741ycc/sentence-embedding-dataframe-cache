from typing import List, Optional, Text

import numpy as np
from jina import Client, DocumentArray

from embedding_store.base import EmbeddingStore


class JinaEmbeddingStore(EmbeddingStore):
    def __init__(self, embedding_grpc: Text, cache_path: Optional[str] = None, batch_size=100) -> None:
        """Retrieve the sentence embedding from deployed Jina service, if the cache is existed then return the cache
        results directly

        Args:
            embedding_grpc (Text): Jina service grpc.
            cache_path (Optional[str], optional): Parquet format cache path. Defaults to None.
            batch_size (int, optional): Maximum size of batch processing from the Jina service. Defaults to 100.
        """
        super().__init__(cache_path)
        self.embedding_grpc = embedding_grpc
        self.batch_size = batch_size

    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        jina_client = Client(host="grpc://0.0.0.0:54321")
        embedding_results = np.array([])

        if len(sentences) > 0:
            document_array = DocumentArray().empty(len(sentences))
            embedding_results = jina_client.post("/", document_array).embeddings

        return embedding_results
