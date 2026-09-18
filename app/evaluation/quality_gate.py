from dataclasses import dataclass

from app.evaluation.evaluator import (
    EvaluationSummary,
)


@dataclass
class QualityThresholds:
    min_recall: float = 0.80
    min_mrr: float = 0.70
    min_hit_rate: float = 0.80
    max_p95_latency_ms: float = 1000.0


class EvaluationGateError(Exception):
    pass


def validate_quality(
    summary: EvaluationSummary,
    thresholds: QualityThresholds,
) -> None:

    failures = []

    if (
        summary.mean_recall_at_k
        < thresholds.min_recall
    ):
        failures.append(
            "Recall below threshold: "
            f"{summary.mean_recall_at_k:.3f} "
            f"< {thresholds.min_recall:.3f}"
        )

    if (
        summary.mean_reciprocal_rank
        < thresholds.min_mrr
    ):
        failures.append(
            "MRR below threshold: "
            f"{summary.mean_reciprocal_rank:.3f} "
            f"< {thresholds.min_mrr:.3f}"
        )

    if (
        summary.mean_hit_rate_at_k
        < thresholds.min_hit_rate
    ):
        failures.append(
            "Hit rate below threshold: "
            f"{summary.mean_hit_rate_at_k:.3f} "
            f"< {thresholds.min_hit_rate:.3f}"
        )

    if (
        summary.p95_latency_ms
        > thresholds.max_p95_latency_ms
    ):
        failures.append(
            "P95 latency above threshold: "
            f"{summary.p95_latency_ms:.1f}ms "
            f"> "
            f"{thresholds.max_p95_latency_ms:.1f}ms"
        )

    if failures:
        raise EvaluationGateError(
            "\n".join(failures)
        )
