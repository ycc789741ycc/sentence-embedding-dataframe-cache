import logging
import os

from jina import Document, DocumentArray, Executor, requests
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

SENTENCE_TRANSFORMER = os.environ.get(
    "SENTENCE_TRANSFORMER", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
if SENTENCE_TRANSFORMER is None:
    raise ValueError("SENTENCE_TRANSFORMER should be defined in environment variable.")

logger.info(f"Loading transformer model: {SENTENCE_TRANSFORMER}")
model = SentenceTransformer(SENTENCE_TRANSFORMER).eval()


class EmbeddingModel(Executor):
    @requests
    def encode(self, docs: DocumentArray, **kwargs):
        docs.embeddings = model.encode(docs.texts)

    @requests(on="/current_model")
    def current_model(self, **kwargs):
        docs = DocumentArray()
        docs.append(Document(text=SENTENCE_TRANSFORMER))
        return docs
