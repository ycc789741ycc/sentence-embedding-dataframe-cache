from typing import List, Literal, Optional, Text

import numpy as np
from sentence_transformers import SentenceTransformer

from embestore.store.base import EmbeddingStore


class TorchEmbeddingStore(EmbeddingStore):
    def __init__(
        self,
        max_size: Optional[int] = None,
        eviction_policy: Optional[Literal["lfu", "lru"]] = None,
        cache_path: Optional[str] = None,
        model_name: Text = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        super().__init__(max_size, eviction_policy, cache_path)
        self.model = SentenceTransformer(model_name).eval()

    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        return self.model.encode(sentences)
