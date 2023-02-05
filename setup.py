# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["embestore", "embestore.store"]

package_data = {"": ["*"]}

install_requires = ["numpy>=1.24.1,<2.0.0", "pandas>=1.5.2,<2.0.0", "pyarrow>=11.0.0,<12.0.0"]

extras_require = {
    "jina": ["jina>=3.13.2,<4.0.0"],
    "sentence-transformers": ["torch>=1.13.1,<2.0.0", "sentence-transformers>=2.2.2,<3.0.0"],
}

setup_kwargs = {
    "name": "embestore",
    "version": "0.2.1",
    "description": "",
    "long_description": (
        "[![Code style:"
        " black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n##"
        " Introduction\n\nImplement the sentence embedding retriever with local cache from the embedding store.\n\n##"
        " Features\n\n* Embedding store abstraction class\n\n* Support [Jina](https://github.com/jina-ai/jina) client"
        " implementation embedding store\n\n* Support LFU, LRU cache eviction policy for limited cache size, if the"
        " eviction policy is not specified then won't\napply any eviction policy\n\n* Save the cache to parquet"
        " file\n\n* Load the cache from existed parquet file\n\n## Quick Start\n\n### **Option 1.** Using Jina flow"
        ' serve the embedding model\n\n* Installation\n\n```bash\npip install embestore"[jina]"\n```\n\n* To start up'
        " the Jina flow service with sentence embedding"
        " model\n`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, you can just clone\nthis github repo"
        " directly and serve by the docker container.\n\n```bash\ngit clone"
        " https://github.com/ycc789741ycc/sentence-embedding-dataframe-cache.git\n\ncd"
        " sentence-embedding-dataframe-cache\n\nmake serve-jina-embedding\n```\n\n* Retrieve the"
        " embedding\n\n```python\nfrom embestore.store.jina import JinaEmbeddingStore\n\nJINA_EMBEDDING_STORE_GRPC ="
        ' "grpc://0.0.0.0:54321"\n\n\nquery_sentences = ["I want to listen the music.", "Music don\'t want to listen'
        ' me."]\n\njina_embedding_store = JinaEmbeddingStore(embedding_grpc=JINA_EMBEDDING_STORE_GRPC)\nembeddings ='
        " jina_embedding_store.retrieve_embeddings(sentences=query_sentences)\n\n>>> embeddings\narray([["
        " 2.26917475e-01,  8.17841291e-02,  2.35427842e-02,\n        -3.02357599e-02,  1.15757119e-02,"
        " -8.42996314e-02,\n         4.42815214e-01,  1.80795133e-01,  1.04702041e-01,\n         ...\n]])\n```\n\n*"
        " Stop the docker container\n\n```bash\nmake stop-jina-embedding\n```\n\n### **Option 2.** Using local sentence"
        ' embedding model\n\n* Installation\n\n```bash\npip install embestore"[sentence-transformers]"\n```\n\n* Serve'
        " the sentence embedding model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` by"
        ' in-memory\n\n```python\nfrom embestore.store.torch import TorchEmbeddingStore\n\nquery_sentences = ["I want'
        ' to listen the music.", "Music don\'t want to listen me."]\n\n\ntorch_embedding_store ='
        " TorchEmbeddingStore()\nembeddings ="
        " torch_embedding_store.retrieve_embeddings(sentences=query_sentences)\n\n>>> embeddings\narray([["
        " 2.26917475e-01,  8.17841291e-02,  2.35427842e-02,\n        -3.02357599e-02,  1.15757119e-02,"
        " -8.42996314e-02,\n         4.42815214e-01,  1.80795133e-01,  1.04702041e-01,\n         ...\n]])\n```\n\n###"
        " **Option 3.** Inherit from the abstraction class\n\n* Installation\n\n```bash\npip install"
        " embestore\n```\n\n```python\nfrom typing import List, Text\n\nimport numpy as np\nfrom sentence_transformers"
        " import SentenceTransformer\n\nfrom embestore.store.base import EmbeddingStore\n\nmodel ="
        ' SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").eval()\n\n\nclass'
        " TorchEmbeddingStore(EmbeddingStore):\n    def _retrieve_embeddings_from_model(self, sentences: List[Text]) ->"
        " np.ndarray:\n        return model.encode(sentences)\n```\n\n### Save the"
        ' cache\n\n```python\ntorch_embedding_store.save("cache.parquet")\n```\n\n### Load from the'
        ' cache\n\n```python\ntorch_embedding_store = TorchEmbeddingStore("cache.parquet")\n```\n\n### Apply eviction'
        " policy\n\n* LRU\n\n```python\ntorch_embedding_store = TorchEmbeddingStore(max_size=100,"
        ' eviction_policy="lru")\n```\n\n* LFU\n\n```python\ntorch_embedding_store = TorchEmbeddingStore(max_size=100,'
        ' eviction_policy="lfu")\n```\n\n## Road Map\n\n[TODO] Documentation\n\n[TODO] Badges\n'
    ),
    "author": "Yoshi Gao",
    "author_email": "yoshi4868686@gmail.com",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "None",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "extras_require": extras_require,
    "python_requires": ">=3.9,<4.0",
}


setup(**setup_kwargs)
