from typing import List, Text

import numpy as np
from sentence_transformers import SentenceTransformer

from embestore.store.base import EmbeddingStore

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").eval()


class TorchEmbeddingStore(EmbeddingStore):
    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        return model.encode(sentences)
