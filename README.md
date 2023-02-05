[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction

Implement the sentence embedding retriever with local cache from the embedding store.

## Features

* Embedding store abstraction class

* Support [Jina](https://github.com/jina-ai/jina) client implementation embedding store

* Support LFU, LRU cache eviction policy for limited cache size, if the eviction policy is not specified then won't
apply any eviction policy

* Save the cache to parquet file

* Load the cache from existed parquet file

## Quick Start

### **Option 1.** Using Jina flow serve the embedding model

* Installation

```bash
pip install embestore"[jina]"
```

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
from embestore.store.jina import JinaEmbeddingStore

JINA_EMBEDDING_STORE_GRPC = "grpc://0.0.0.0:54321"


query_sentences = ["I want to listen the music.", "Music don't want to listen me."]

jina_embedding_store = JinaEmbeddingStore(embedding_grpc=JINA_EMBEDDING_STORE_GRPC)
embeddings = jina_embedding_store.retrieve_embeddings(sentences=query_sentences)

>>> embeddings
array([[ 2.26917475e-01,  8.17841291e-02,  2.35427842e-02,
        -3.02357599e-02,  1.15757119e-02, -8.42996314e-02,
         4.42815214e-01,  1.80795133e-01,  1.04702041e-01,
         ...
]])
```

* Stop the docker container

```bash
make stop-jina-embedding
```

### **Option 2.** Using local sentence embedding model

* Installation

```bash
pip install embestore"[sentence-transformers]"
```

* Serve the sentence embedding model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` by in-memory

```python
from embestore.store.torch import TorchEmbeddingStore

query_sentences = ["I want to listen the music.", "Music don't want to listen me."]


torch_embedding_store = TorchEmbeddingStore()
embeddings = torch_embedding_store.retrieve_embeddings(sentences=query_sentences)

>>> embeddings
array([[ 2.26917475e-01,  8.17841291e-02,  2.35427842e-02,
        -3.02357599e-02,  1.15757119e-02, -8.42996314e-02,
         4.42815214e-01,  1.80795133e-01,  1.04702041e-01,
         ...
]])
```

### **Option 3.** Inherit from the abstraction class

* Installation

```bash
pip install embestore
```

```python
from typing import List, Text

import numpy as np
from sentence_transformers import SentenceTransformer

from embestore.store.base import EmbeddingStore

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").eval()


class TorchEmbeddingStore(EmbeddingStore):
    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        return model.encode(sentences)
```

### Save the cache

```python
torch_embedding_store.save("cache.parquet")
```

### Load from the cache

```python
torch_embedding_store = TorchEmbeddingStore("cache.parquet")
```

### Apply eviction policy

* LRU

```python
torch_embedding_store = TorchEmbeddingStore(max_size=100, eviction_policy="lru")
```

* LFU

```python
torch_embedding_store = TorchEmbeddingStore(max_size=100, eviction_policy="lfu")
```

## Road Map

[TODO] Documentation

[TODO] Badges
