from typing import List

from sentence_transformers import CrossEncoder

from app.retrieval.hybrid_search import HybridResult


class CrossEncoderReranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: List[HybridResult],
        top_k: int = 5,
    ) -> List[HybridResult]:

        if not results:
            return []

        pairs = [
            [query, result.text]
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = sorted(
            zip(results, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        output = []

        for result, score in reranked[:top_k]:

            output.append(
                HybridResult(
                    chunk_id=result.chunk_id,
                    text=result.text,
                    score=float(score),
                )
            )

        return output
