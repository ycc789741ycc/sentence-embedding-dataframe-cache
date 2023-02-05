import math
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Literal, Optional, Text

import numpy as np
import pandas as pd

VALID_ROW_ATTRIBUTE = "sentence"
VALID_COLUMN_ATTRIBUTE = "embedding"
LFU_COUNTER_COLUMN = "count"


class EvictionPolicy(str, Enum):
    LFU = "lfu"
    LRU = "lru"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class EmbeddingStore(ABC):
    """Retrieve sentence embeddings."""

    def __init__(
        self,
        max_size: Optional[int] = None,
        eviction_policy: Optional[Literal["lfu", "lru"]] = None,
        cache_path: Optional[str] = None,
    ) -> None:
        def create_empty_df() -> pd.DataFrame:
            df = pd.DataFrame({VALID_ROW_ATTRIBUTE: [], VALID_COLUMN_ATTRIBUTE: [], LFU_COUNTER_COLUMN: []})
            df.set_index(VALID_ROW_ATTRIBUTE, inplace=True)

            return df

        if eviction_policy is not None:
            if not EvictionPolicy.has_value(eviction_policy):
                raise ValueError(
                    "eviction_policy should be within " + ", ".join([policy.value for policy in EvictionPolicy])
                )
            if max_size is None:
                raise ValueError("max_size can't be None")
        if max_size is not None:
            if max_size <= 0:
                raise ValueError("max_size must be larger than 0")
            if eviction_policy is None:
                raise ValueError("eviction_policy can't be None")

        self._max_size = max_size
        self._eviction_policy = eviction_policy
        self.cache_path = cache_path

        if self.cache_path is None or not os.path.isfile(cache_path):
            self.cache_df = create_empty_df()
        else:
            self.cache_df = pd.read_parquet(cache_path)
            self._column_validation(self.cache_df)

    @property
    def eviction_policy(self) -> Text:
        return self._eviction_policy

    @property
    def max_size(self) -> int:
        return self._max_size

    def _column_validation(self, df: pd.DataFrame) -> None:
        if VALID_ROW_ATTRIBUTE != df.index.name:
            raise ValueError(f"Missing row index: {VALID_ROW_ATTRIBUTE}")
        if VALID_COLUMN_ATTRIBUTE not in df.columns:
            raise ValueError(f"Missing column index: {VALID_COLUMN_ATTRIBUTE}")
        if LFU_COUNTER_COLUMN not in df.columns:
            raise ValueError(f"Missing column index: {LFU_COUNTER_COLUMN}")
        if len(df.columns) != 2:
            raise ValueError("Column size should be 2")

    def retrieve_dataframe_embeddings(self, sentences: List[Text]) -> pd.DataFrame:
        """Retrieve the sentence embeddings from the cache, if the sentence embedding doesn't
        existed in cache then search result from the model. Return the sentence embeddings
        from the cache, if the sentence embedding doesn't existed in cache then search result from the model.
        """

        embeddings_df = self._retrieve_embeddings_from_cache(sentences)
        null_value_mask = embeddings_df[VALID_COLUMN_ATTRIBUTE].isnull()
        embeddings_from_model = self._retrieve_embeddings_from_model(
            sentences=embeddings_df.index[null_value_mask].to_list()
        )
        embeddings_df[VALID_COLUMN_ATTRIBUTE].loc[null_value_mask] = [
            np.array(v) for v in embeddings_from_model.tolist()
        ]
        embeddings_df[LFU_COUNTER_COLUMN] = embeddings_df[LFU_COUNTER_COLUMN].apply(lambda x: x + 1)

        self._update_cache_df(new_embedding_df=embeddings_df)
        self._apply_eviction_policy()

        return embeddings_df

    def _update_cache_df(self, new_embedding_df: pd.DataFrame) -> None:
        self._column_validation(self.cache_df)
        self._column_validation(new_embedding_df)
        self.cache_df = pd.concat([self.cache_df, new_embedding_df], axis=0)
        self.cache_df = self.cache_df.loc[~self.cache_df.index.duplicated(keep="last")]

    def _apply_eviction_policy(self) -> None:
        if self._eviction_policy is not None and len(self.cache_df) > self._max_size:
            keeped_size = self.max_size
            if self._eviction_policy == EvictionPolicy.LRU.value:
                keeped_size = self.max_size
            elif self._eviction_policy == EvictionPolicy.LFU.value:
                keeped_size = math.ceil(self._max_size / 2)
                self.cache_df.sort_values(LFU_COUNTER_COLUMN, inplace=True)
            else:
                raise ValueError("Unknown eviction policy")

            self.cache_df = self.cache_df.iloc[-keeped_size:]

    def retrieve_embeddings(self, sentences: List[Text]) -> np.ndarray:
        """Retrieve the sentence embeddings from the cache, if the sentence embedding doesn't
        existed in cache then search result from the model.
        """

        return np.array(self.retrieve_dataframe_embeddings(sentences=sentences)[VALID_COLUMN_ATTRIBUTE].to_list())

    def _retrieve_embeddings_from_cache(self, sentences: List[Text]) -> pd.DataFrame:
        sentences_df = pd.DataFrame({VALID_ROW_ATTRIBUTE: sentences})
        embeddings_df = sentences_df.merge(
            self.cache_df[~self.cache_df.index.duplicated(keep="first")].reset_index(),
            how="left",
            on=VALID_ROW_ATTRIBUTE,
        )
        embeddings_df[VALID_COLUMN_ATTRIBUTE].replace({np.nan: None}, inplace=True)
        embeddings_df[LFU_COUNTER_COLUMN].replace({np.nan: 0}, inplace=True)
        embeddings_df.set_index(VALID_ROW_ATTRIBUTE, inplace=True)

        return embeddings_df

    def save(self, path: Optional[str] = None):
        """Save the cache to parquet."""

        if path is not None:
            self.cache_df.to_parquet(path)
        else:
            if self.cache_path is None:
                raise ValueError("Miss the path to save the file!")
            self.cache_df.to_parquet(self.cache_path)

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
