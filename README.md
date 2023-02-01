[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction

Implement the sentence embedding retriever with local cache from the embedding store.

## Features

* Embedding store abstraction class

* Support Jina client implementation embedding store

## Installation

```bash
```

## Quick Start

### Using Jina flow serve the embedding model

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
from embedding_store.jina import JinaEmbeddingStore


JINA_EMBEDDING_STORE_GRPC = "grpc://0.0.0.0:54321"


query_sentences = ["I want to listen the music.", "Music don't want to listen me."]

jina_embedding_store = JinaEmbeddingStore(embedding_grpc=JINA_EMBEDDING_STORE_GRPC)
results = jina_embedding_store.retrieve_embeddings(sentences=query_sentences)
```

* Stop the docker container

```bash
stop-jina-embedding
```

### Inherit from the abstraction class

```python
```

# Road Map

[Done] prototype abstraction

[Done] Unit-test, integration test

[Todo] Embedding retriever implementation: Pytorch, Jina

* [Done] Jina

* [Todo] Sentence Embedding

[Done] Docker service

[Todo] Example, Documentation

[Todo] Embedding monitor

[Todo] pip install support

[Improve] Accelerate the Pandas retriever efficiency
