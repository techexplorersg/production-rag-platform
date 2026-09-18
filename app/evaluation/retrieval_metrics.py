from typing import Iterable, Sequence


def recall_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: Iterable[str],
    k: int,
) -> float:
    """
    Fraction of relevant documents retrieved within top-k.
    """

    relevant = set(relevant_ids)

    if not relevant:
        return 0.0

    retrieved = set(retrieved_ids[:k])

    return len(retrieved & relevant) / len(relevant)


def reciprocal_rank(
    retrieved_ids: Sequence[str],
    relevant_ids: Iterable[str],
) -> float:
    """
    Reciprocal rank of the first relevant result.
    """

    relevant = set(relevant_ids)

    for rank, chunk_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if chunk_id in relevant:
            return 1.0 / rank

    return 0.0


def hit_rate_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: Iterable[str],
    k: int,
) -> float:
    """
    Returns 1 when at least one relevant result
    appears in the top-k.
    """

    relevant = set(relevant_ids)

    return float(
        any(
            chunk_id in relevant
            for chunk_id in retrieved_ids[:k]
        )
    )
