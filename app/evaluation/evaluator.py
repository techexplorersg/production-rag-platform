import json
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Callable, List

from app.evaluation.retrieval_metrics import (
    hit_rate_at_k,
    recall_at_k,
    reciprocal_rank,
)


@dataclass
class EvaluationResult:
    query_id: str
    query: str
    recall_at_k: float
    reciprocal_rank: float
    hit_rate_at_k: float
    latency_ms: float


@dataclass
class EvaluationSummary:
    total_queries: int
    mean_recall_at_k: float
    mean_reciprocal_rank: float
    mean_hit_rate_at_k: float
    mean_latency_ms: float
    p95_latency_ms: float


class RetrievalEvaluator:

    def __init__(
        self,
        retriever: Callable[[str, int], List[str]],
        top_k: int = 5,
    ):
        self.retriever = retriever
        self.top_k = top_k

    def load_dataset(
        self,
        path: str,
    ):
        dataset_path = Path(path)

        with dataset_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def evaluate_query(
        self,
        example: dict,
    ) -> EvaluationResult:

        start = time.perf_counter()

        retrieved_ids = self.retriever(
            example["query"],
            self.top_k,
        )

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        relevant_ids = example[
            "relevant_chunk_ids"
        ]

        return EvaluationResult(
            query_id=example["query_id"],
            query=example["query"],
            recall_at_k=recall_at_k(
                retrieved_ids,
                relevant_ids,
                self.top_k,
            ),
            reciprocal_rank=reciprocal_rank(
                retrieved_ids,
                relevant_ids,
            ),
            hit_rate_at_k=hit_rate_at_k(
                retrieved_ids,
                relevant_ids,
                self.top_k,
            ),
            latency_ms=latency_ms,
        )

    def evaluate(
        self,
        dataset_path: str,
    ):
        dataset = self.load_dataset(
            dataset_path
        )

        results = [
            self.evaluate_query(example)
            for example in dataset
        ]

        summary = self._summarize(
            results
        )

        return results, summary

    @staticmethod
    def _percentile(
        values,
        percentile: float,
    ) -> float:

        if not values:
            return 0.0

        ordered = sorted(values)

        index = int(
            round(
                (len(ordered) - 1)
                * percentile
            )
        )

        return ordered[index]

    def _summarize(
        self,
        results: List[EvaluationResult],
    ) -> EvaluationSummary:

        if not results:
            return EvaluationSummary(
                total_queries=0,
                mean_recall_at_k=0.0,
                mean_reciprocal_rank=0.0,
                mean_hit_rate_at_k=0.0,
                mean_latency_ms=0.0,
                p95_latency_ms=0.0,
            )

        latencies = [
            result.latency_ms
            for result in results
        ]

        return EvaluationSummary(
            total_queries=len(results),

            mean_recall_at_k=mean(
                result.recall_at_k
                for result in results
            ),

            mean_reciprocal_rank=mean(
                result.reciprocal_rank
                for result in results
            ),

            mean_hit_rate_at_k=mean(
                result.hit_rate_at_k
                for result in results
            ),

            mean_latency_ms=mean(
                latencies
            ),

            p95_latency_ms=self._percentile(
                latencies,
                0.95,
            ),
        )
