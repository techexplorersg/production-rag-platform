# ADR-002: Use Reciprocal Rank Fusion

**Status:** Accepted

## Context

Dense retrieval and BM25 generate scores with different meanings and
numerical distributions.

Directly adding their raw scores would require normalization and can make
fusion sensitive to retriever-specific score ranges.

## Decision

Use Reciprocal Rank Fusion (RRF) to combine candidate rankings.

For a document d:

RRF(d) = Σ 1 / (k + rank(d))

The implementation therefore combines ranking positions rather than raw
retriever scores.

## Alternatives Considered

- Raw score addition
- Min-max score normalization
- Weighted normalized fusion
- Learned ranking/fusion model

## Trade-offs

RRF is simple, deterministic, and independent of score calibration.

However, it discards information contained in the magnitude of individual
retriever scores and introduces a fusion parameter that still requires
evaluation.

## Consequences

Retrievers remain independently replaceable while exposing a common
rank-based fusion layer.

Future experiments can compare RRF against weighted or learned fusion
using the same evaluation dataset.
