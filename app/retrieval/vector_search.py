from dataclasses import dataclass
from typing import List

import faiss
import numpy as np

from app.ingestion.chunker import Chunk


@dataclass
class SearchResult:
    chunk: Chunk
    score: float


class VectorRetriever:

    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: List[Chunk] = []

    def add(
        self,
        chunks: List[Chunk],
        embeddings: np.ndarray,
    ) -> None:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match"
            )

        self.index.add(
            embeddings.astype("float32")
        )

        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 10,
    ) -> List[SearchResult]:

        if self.index.ntotal == 0:
            return []

        k = min(
            top_k,
            self.index.ntotal,
        )

        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            results.append(
                SearchResult(
                    chunk=self.chunks[index],
                    score=float(score),
                )
            )

        return results
