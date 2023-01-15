import os
from abc import ABC, abstractmethod
from typing import List, Optional, Text

import numpy as np
import pandas as pd

VALID_ROW_ATTRIBUTE = "sentence"
VALID_COLUMN_ATTRIBUTE = "embedding"


class EmbeddingStore(ABC):
    """Retrieve sentence embeddings."""

    def __init__(self, parquet_file_path: Optional[str] = None) -> None:
        def create_empty_df() -> pd.DataFrame:
            df = pd.DataFrame({VALID_ROW_ATTRIBUTE: [], VALID_COLUMN_ATTRIBUTE: []})
            df.set_index(VALID_ROW_ATTRIBUTE, inplace=True)

            return df

        self.parquet_file_path = parquet_file_path

        if self.parquet_file_path is None:
            self.cache_df = create_empty_df()
        else:
            if os.path.isfile(parquet_file_path):
                self.cache_df = pd.read_parquet(parquet_file_path)
                self._column_validation(self.cache_df)
            else:
                self.cache_df = create_empty_df()
                self.cache_df.to_parquet(parquet_file_path)

    def _column_validation(self, df: pd.DataFrame) -> None:
        if VALID_ROW_ATTRIBUTE != df.index.name:
            raise ValueError(f"Missing row index: {VALID_ROW_ATTRIBUTE}")
        if VALID_COLUMN_ATTRIBUTE not in df.columns:
            raise ValueError(f"Missing column index: {VALID_COLUMN_ATTRIBUTE}")
        if len(df.columns) != 1:
            raise ValueError("Column size should be 1")

    def _update_cache_df(self, new_embedding_df: pd.DataFrame) -> None:
        self._column_validation(self.cache_df)
        self._column_validation(new_embedding_df)
        self.cache_df = pd.concat([self.cache_df, new_embedding_df], axis=0)
        self.cache_df = self.cache_df.loc[~self.cache_df.index.duplicated(keep="last")]

    def retrieve_embeddings(self, sentences: List[Text]) -> np.ndarray:
        """Retrieve the sentence embeddings from the cache, if the sentence embedding doesn't
        existed in cache then search result from the model.
        """

        return np.array(self.retrieve_dataframe_embeddings(sentences=sentences)[VALID_COLUMN_ATTRIBUTE].to_list())

    def retrieve_dataframe_embeddings(self, sentences: List[Text]) -> pd.DataFrame:
        """Retrieve the sentence embeddings from the cache, if the sentence embedding doesn't
        existed in cache then search result from the model. Return the sentence embeddings
        from the cache, if the sentence embedding doesn't existed in cache then search result from the model.
        """
        # TODO Accelerate the pandas speed

        sentences_df = pd.DataFrame({VALID_ROW_ATTRIBUTE: sentences})
        embeddings_df = sentences_df.merge(
            self.cache_df[~self.cache_df.index.duplicated(keep="first")].reset_index(),
            how="left",
            on=VALID_ROW_ATTRIBUTE,
        )
        embeddings_df.replace({np.nan: None}, inplace=True)
        embeddings_df.set_index(VALID_ROW_ATTRIBUTE, inplace=True)

        null_value_mask = embeddings_df[VALID_COLUMN_ATTRIBUTE].isnull()
        embeddings_from_model = self._retrieve_embeddings_from_model(
            sentences=embeddings_df.index[null_value_mask].to_list()
        )
        embeddings_df[VALID_COLUMN_ATTRIBUTE].loc[null_value_mask] = [
            np.array(v) for v in embeddings_from_model.tolist()
        ]
        self._update_cache_df(new_embedding_df=embeddings_df)

        return embeddings_df

    def save(self, path: Optional[str] = None):
        """Save the cache to parquet."""

        if path is not None:
            self.cache_df.to_parquet(path)
        else:
            if self.parquet_file_path is None:
                raise ValueError("Miss the path to save the file!")
            self.cache_df.to_parquet(self.parquet_file_path)

    def _get_embeddings_from_cache(self, keys: List[Text]) -> Optional[np.ndarray]:
        """Search the cache result from the cache dataframe.

        Parameters
        ----------
        keys : Text
            The key to index the cache value.

        Returns
        -------
        Optional[np.ndarray]
            Embedding results.
        """

        results = self.cache_df.loc[self.cache_df.index.isin(keys), VALID_COLUMN_ATTRIBUTE].to_list()

        return np.array(results) if len(results) > 0 else None

    @abstractmethod
    def _retrieve_embeddings_from_model(self, sentences: List[Text]) -> np.ndarray:
        """Retrieve the embedding results from the customized model.

        Parameters
        ----------
        sentences : List[Text]
            Sentences to embed.

        Returns
        -------
        np.ndarray
            Embedding results.
        """

        pass
