# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["embestore"]

package_data = {"": ["*"]}

install_requires = ["numpy>=1.24.1,<2.0.0", "pandas>=1.5.2,<2.0.0", "pyarrow>=11.0.0,<12.0.0"]

setup_kwargs = {
    "name": "embestore",
    "version": "0.1.2",
    "description": "",
    "long_description": (
        "[![Code style:"
        " black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n##"
        " Introduction\n\nImplement the sentence embedding retriever with local cache from the embedding store.\n\n##"
        " Features\n\n* Embedding store abstraction class\n\n* Support Jina client implementation embedding store\n\n*"
        " Save the cache to parquet file\n\n* Load the cache from existed parquet file\n\n##"
        " Installation\n\n```bash\n```\n\n## Quick Start\n\n### **Option 1.** Using Jina flow serve the embedding"
        " model\n\n* To start up the Jina flow service with sentence embedding"
        " model\n`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, you can just clone\nthis github repo"
        " directly and serve by the docker container.\n\n```bash\ngit clone"
        " https://github.com/ycc789741ycc/sentence-embedding-dataframe-cache.git\n\ncd"
        " sentence-embedding-dataframe-cache\n\nmake serve-jina-embedding\n```\n\n* Retrieve the"
        " embedding\n\n```python\nfrom embestore.jina import JinaEmbeddingStore\n\nJINA_embestore_GRPC ="
        ' "grpc://0.0.0.0:54321"\n\n\nquery_sentences = ["I want to listen the music.", "Music don\'t want to listen'
        ' me."]\n\njina_embestore = JinaEmbeddingStore(embedding_grpc=JINA_embestore_GRPC)\nresults ='
        " jina_embestore.retrieve_embeddings(sentences=query_sentences)\n```\n\n* Stop the docker"
        " container\n\n```bash\nstop-jina-embedding\n```\n\n### **Option 2.** Using local sentence embedding model"
        " `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`\n\n```python\nfrom embestore.torch import"
        ' TorchEmbeddingStore\n\nquery_sentences = ["I want to listen the music.", "Music don\'t want to listen'
        ' me."]\n\n\ntorch_embestore = TorchEmbeddingStore()\nresults ='
        " torch_embestore.retrieve_embeddings(sentences=query_sentences)\n```\n\n### **Option 3.** Inherit from the"
        " abstraction class\n\n```python\nfrom typing import List, Text\n\nimport numpy as np\nfrom"
        " sentence_transformers import SentenceTransformer\n\nfrom embestore.base import EmbeddingStore\n\nmodel ="
        ' SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").eval()\n\n\nclass'
        " TorchEmbeddingStore(EmbeddingStore):\n    def _retrieve_embeddings_from_model(self, sentences: List[Text]) ->"
        " np.ndarray:\n        return model.encode(sentences)\n```\n\n### Save the"
        ' cache\n\n```python\ntorch_embestore.save("cache.parquet")\n```\n\n### Load from the'
        ' cache\n\n```python\ntorch_embestore = TorchEmbeddingStore("cache.parquet")\n```\n\n# Road Map\n\n[Done]'
        " prototype abstraction\n\n[Done] Unit-test, integration test\n\n[Done] Embedding retriever implementation:"
        " Pytorch, Jina\n\n* [Done] Jina\n\n* [Done] Sentence Embedding\n\n[Done] Docker service\n\n[Todo] Example,"
        " Documentation\n\n[Todo] Embedding monitor\n\n[Todo] pip install support\n\n[Improve] Accelerate the Pandas"
        " retriever efficiency\n"
    ),
    "author": "Yoshi Gao",
    "author_email": "yoshi4868686@gmail.com",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "None",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.9,<4.0",
}


setup(**setup_kwargs)
