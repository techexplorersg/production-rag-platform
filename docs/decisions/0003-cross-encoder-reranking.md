# ADR-003: Use Two-Stage Retrieval with Cross-Encoder Reranking

**Status:** Accepted

## Context

Bi-encoder embeddings enable efficient retrieval because document
embeddings can be calculated in advance.

However, query and document representations are produced independently.

A cross-encoder jointly evaluates the query and candidate text and can
provide a stronger relevance signal, but at substantially higher
computational cost.

## Decision

Use inexpensive retrieval to generate a limited candidate set and apply
cross-encoder reranking only to those candidates.

Pipeline:

Query
  |
  +---- Dense Retrieval
  |
  +---- BM25
          |
          v
         RRF
          |
          v
   Candidate Set
          |
          v
    Cross Encoder
          |
          v
      Top Context

## Alternatives Considered

- No reranking
- LLM-based reranking
- Larger embedding model
- Learned ranking model

## Trade-offs

Benefits:
- More expressive query-document relevance scoring
- Clean separation between candidate generation and ranking

Costs:
- Additional inference latency
- Additional model dependency
- Increased compute requirements

## Operational Implication

Candidate-set size becomes an explicit latency/quality trade-off.

Changes to candidate size or reranking models should therefore be
benchmarked for both retrieval quality and latency before adoption.
