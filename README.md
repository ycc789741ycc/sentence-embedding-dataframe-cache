[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction

Implement the sentence embedding retriever with local cache from the embedding store.

## Features

* Embedding store abstraction class

* Support Jina client implementation embedding store

* Save the cache to parquet file

* Load the cache from existed parquet file

## Installation

```bash
```

## Quick Start

### **Option 1.** Using Jina flow serve the embedding model

* To start up the Jina flow service with sentence embedding model
`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, you can just clone
this github repo directly and serve by the docker container.

```bash
git clone https://github.com/ycc789741ycc/sentence-embedding-dataframe-cache.git

cd sentence-embedding-dataframe-cache

make serve-jina-embedding
```

* Retrieve the embedding

```python
from embestore.jina import JinaEmbeddingStore

JINA_EMBESTORE_GRPC = "grpc://0.0.0.0:54321"


query_sentences = ["I want to listen the music.", "Music don't want to listen me."]

jina_embestore = JinaEmbeddingStore(embedding_grpc=JINA_EMBESTORE_GRPC)
results = jina_embestore.retrieve_embeddings(sentences=query_sentences)
```

* Stop the docker container

```bash
stop-jina-embedding
```

### **Option 2.** Using local sentence embedding model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

```python
from embestore.torch import TorchEmbeddingStore

query_sentences = ["I want to listen the music.", "Music don't want to listen me."]


torch_embestore = TorchEmbeddingStore()
results = torch_embestore.retrieve_embeddings(sentences=query_sentences)
```

### **Option 3.** Inherit from the abstraction class

```python
from typing import List, Text

import numpy as np
from sentence_transformers import SentenceTransformer

from embestore.base import EmbeddingStore

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").eval()


class TorchEmbeddingStore(EmbeddingStore):
    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        return model.encode(sentences)
```

### Save the cache

```python
torch_embestore.save("cache.parquet")
```

### Load from the cache

```python
torch_embestore = TorchEmbeddingStore("cache.parquet")
```

# Road Map

[Done] prototype abstraction

[Done] Unit-test, integration test

[Done] Embedding retriever implementation: Pytorch, Jina

* [Done] Jina

* [Done] Sentence Embedding

[Done] Docker service

[Todo] Example, Documentation

[Todo] Embedding monitor

[Todo] pip install support

[Improve] Accelerate the Pandas retriever efficiency
