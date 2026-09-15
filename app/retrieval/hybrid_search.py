from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HybridResult:
    chunk_id: str
    text: str
    score: float


class HybridRetriever:

    def __init__(
        self,
        vector_retriever,
        keyword_retriever,
        rrf_k: int = 60,
    ):
        self.vector = vector_retriever
        self.keyword = keyword_retriever
        self.rrf_k = rrf_k

    def search(
        self,
        query: str,
        query_embedding,
        top_k: int = 10,
    ) -> List[HybridResult]:

        vector_results = self.vector.search(
            query_embedding,
            top_k=top_k,
        )

        keyword_results = self.keyword.search(
            query,
            top_k=top_k,
        )

        scores: Dict[str, float] = {}
        chunks = {}

        for rank, result in enumerate(
            vector_results,
            start=1,
        ):
            chunk_id = result.chunk.chunk_id

            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1 / (self.rrf_k + rank)
            )

            chunks[chunk_id] = result.chunk

        for rank, result in enumerate(
            keyword_results,
            start=1,
        ):
            chunk_id = result.chunk.chunk_id

            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1 / (self.rrf_k + rank)
            )

            chunks[chunk_id] = result.chunk

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            HybridResult(
                chunk_id=chunk_id,
                text=chunks[chunk_id].text,
                score=score,
            )
            for chunk_id, score in ranked[:top_k]
        ]
