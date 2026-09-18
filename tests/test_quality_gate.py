import pytest

from app.evaluation.evaluator import (
    EvaluationSummary,
)
from app.evaluation.quality_gate import (
    EvaluationGateError,
    QualityThresholds,
    validate_quality,
)


def test_quality_gate_passes():

    summary = EvaluationSummary(
        total_queries=100,
        mean_recall_at_k=0.91,
        mean_reciprocal_rank=0.84,
        mean_hit_rate_at_k=0.94,
        mean_latency_ms=120,
        p95_latency_ms=240,
    )

    validate_quality(
        summary,
        QualityThresholds(),
    )


def test_quality_gate_fails():

    summary = EvaluationSummary(
        total_queries=100,
        mean_recall_at_k=0.50,
        mean_reciprocal_rank=0.40,
        mean_hit_rate_at_k=0.60,
        mean_latency_ms=500,
        p95_latency_ms=1500,
    )

    with pytest.raises(
        EvaluationGateError
    ):
        validate_quality(
            summary,
            QualityThresholds(),
        )
