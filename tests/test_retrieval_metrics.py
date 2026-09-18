import pytest

from app.evaluation.retrieval_metrics import (
    hit_rate_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k():

    retrieved = [
        "chunk-1",
        "chunk-2",
        "chunk-3",
    ]

    relevant = {
        "chunk-2",
        "chunk-4",
    }

    score = recall_at_k(
        retrieved,
        relevant,
        k=3,
    )

    assert score == pytest.approx(0.5)


def test_reciprocal_rank():

    retrieved = [
        "chunk-1",
        "chunk-2",
        "chunk-3",
    ]

    relevant = {
        "chunk-2"
    }

    score = reciprocal_rank(
        retrieved,
        relevant,
    )

    assert score == pytest.approx(0.5)


def test_hit_rate_at_k():

    retrieved = [
        "chunk-1",
        "chunk-2",
        "chunk-3",
    ]

    relevant = {
        "chunk-3"
    }

    assert hit_rate_at_k(
        retrieved,
        relevant,
        k=2,
    ) == 0.0

    assert hit_rate_at_k(
        retrieved,
        relevant,
        k=3,
    ) == 1.0
