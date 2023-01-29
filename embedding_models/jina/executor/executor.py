from jina import DocumentArray, Executor, requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


class EmbeddingModel(Executor):
    @requests
    def encode(self, docs: DocumentArray, **kwargs):
        docs.embeddings = model.encode(docs.texts)
