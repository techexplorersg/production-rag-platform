from dataclasses import dataclass
from typing import List

from rank_bm25 import BM25Okapi

from app.ingestion.chunker import Chunk


@dataclass
class KeywordResult:
    chunk: Chunk
    score: float


class BM25Retriever:

    def __init__(self):
        self.chunks: List[Chunk] = []
        self.bm25 = None

    @staticmethod
    def tokenize(text: str):
        return text.lower().split()

    def build(
        self,
        chunks: List[Chunk],
    ) -> None:

        self.chunks = chunks

        tokenized_corpus = [
            self.tokenize(chunk.text)
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(
            tokenized_corpus
        )

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> List[KeywordResult]:

        if not self.bm25:
            return []

        tokens = self.tokenize(query)

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        return [
            KeywordResult(
                chunk=self.chunks[index],
                score=float(score),
            )
            for index, score in ranked
        ]
