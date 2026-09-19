# Production RAG Platform

> A production-oriented reference implementation for building, evaluating,
> and operating Retrieval-Augmented Generation systems beyond the prototype stage.

## Why This Project Exists

A basic RAG demo can be built quickly:

Document → Embedding → Vector Search → LLM

Production-oriented RAG introduces harder engineering problems:

- How do we combine semantic and lexical retrieval?
- How do we rerank candidates?
- How do we measure retrieval quality?
- How do we detect regressions?
- How do we trace sources used to generate an answer?
- How do we monitor latency and failures?
- How do we replace model providers without rewriting the application?

This repository explores those engineering concerns as a modular reference implementation.

> **Portfolio note:** This is an independent reference implementation created
> to demonstrate AI/ML system-design patterns. It is not presented as client
> or employer production work.

## System Capabilities

| Capability | Implementation |
|---|---|
| Semantic retrieval | Sentence Transformers + FAISS |
| Lexical retrieval | BM25 |
| Hybrid search | Reciprocal Rank Fusion |
| Reranking | Cross-encoder |
| API layer | FastAPI |
| Retrieval evaluation | Recall@K, MRR, Hit Rate@K |
| Regression protection | Configurable quality gates |
| Latency evaluation | Mean + P95 |
| Testing | pytest |
| CI | GitHub Actions |
| Deployment | Docker |

## Retrieval Pipeline

Query
  │
  ├─────────────┐
  ▼             ▼
Dense Search   BM25
  │             │
  └──────┬──────┘
         ▼
        RRF
         │
         ▼
 Cross-Encoder
    Reranking
         │
         ▼
 Grounded Context
         │
         ▼
        LLM
         │
         ▼
Answer + Sources

## Engineering Decisions

### Why hybrid retrieval?

Dense retrieval captures semantic similarity while BM25 remains effective
for exact terminology, identifiers, acronyms, and keyword-heavy queries.

### Why Reciprocal Rank Fusion?

Dense similarity scores and BM25 scores are not directly comparable.
RRF combines ranking positions instead of naively adding heterogeneous scores.

### Why rerank?

The first-stage retrievers optimize candidate discovery. A cross-encoder
can perform a more expensive query-document relevance calculation over
the smaller candidate set.

### Why evaluate retrieval separately?

When a RAG response fails, the failure may originate in retrieval,
ranking, context construction, or generation. Measuring retrieval
independently makes those failures easier to isolate.

## Evaluation Strategy

Changes to chunking, embedding models, retrieval parameters, fusion logic,
or reranking should be evaluated against a version-controlled golden dataset.

Measured dimensions include:

- Recall@K
- Mean Reciprocal Rank
- Hit Rate@K
- Mean retrieval latency
- P95 retrieval latency

Quality thresholds can be used as regression gates before changes are accepted.

## Quick Start

```bash
git clone https://github.com/techexplorersg/production-rag-platform.git
cd production-rag-platform

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pytest -v
```

# production-rag-platform
Production-grade RAG reference architecture with hybrid retrieval, reranking, grounded generation, evaluation, observability, and FastAPI serving.

                         ┌───────────────┐
                         │     Client    │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         └───────┬───────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │ Query Orchestrator  │
                      └──────────┬──────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
            ┌──────────────┐           ┌──────────────┐
            │ Vector Search│           │Keyword Search│
            └──────┬───────┘           └──────┬───────┘
                   │                          │
                   └────────────┬─────────────┘
                                ▼
                       ┌─────────────────┐
                       │ Hybrid Retrieval│
                       └────────┬────────┘
                                ▼
                         ┌────────────┐
                         │  Reranker  │
                         └─────┬──────┘
                               ▼
                     ┌──────────────────┐
                     │ Context Builder  │
                     └────────┬─────────┘
                              ▼
                         ┌──────────┐
                         │   LLM    │
                         └────┬─────┘
                              ▼
                    ┌───────────────────┐
                    │ Grounded Response │
                    │   + Citations     │
                    └─────────┬─────────┘
                              ▼
              ┌────────────────────────────┐
              │ Evaluation & Observability │
              └────────────────────────────┘


Design goal: This project explores the engineering patterns required to move RAG beyond a prototype: retrieval quality, reranking, grounded generation, evaluation, observability, API serving, testing, and reproducible deployment.


## 📊 Evaluation & Regression Testing

Retrieval quality is treated as a measurable system property rather than a subjective assessment.

The evaluation layer uses a version-controlled golden dataset to measure retrieval behavior across changes to chunking, embedding models, retrieval strategies, fusion parameters, and reranking.

### Retrieval Metrics

| Metric       | Purpose                                                                  |
| ------------ | ------------------------------------------------------------------------ |
| Recall@K     | Measures how much relevant context is retrieved within the top K results |
| MRR          | Measures how highly the first relevant result is ranked                  |
| Hit Rate@K   | Measures whether at least one relevant result appears within the top K   |
| Mean Latency | Tracks average retrieval response time                                   |
| P95 Latency  | Tracks tail retrieval latency                                            |

### Evaluation Pipeline

```text
Code / Configuration Change
            │
            ▼
       Unit Tests
            │
            ▼
      Golden Dataset
            │
            ▼
    Retrieval Pipeline
            │
            ▼
   Evaluation Framework
            │
     ┌──────┼────────┐
     ▼      ▼        ▼
 Recall@K  MRR    Hit Rate
     │      │        │
     └──────┼────────┘
            │
            ▼
      Latency Metrics
            │
            ▼
       Quality Gate
         /      \
      PASS      FAIL
       │          │
       ▼          ▼
    Eligible    Regression
    for Merge    Detected
```

The architecture is designed so different retrieval strategies can be evaluated behind the same interface, enabling controlled comparisons between vector search, lexical retrieval, hybrid retrieval, and reranked retrieval.

> Thresholds and example values used in tests are engineering fixtures unless explicitly identified as measured benchmark results. This repository is a reference implementation rather than a claim about a client or production deployment.

## 🧠 Architecture Decisions

Significant design decisions are documented as Architecture Decision
Records rather than being hidden inside implementation details.

| Decision | Rationale |
|---|---|
| Hybrid Retrieval | Combine semantic and lexical retrieval failure modes |
| Reciprocal Rank Fusion | Fuse heterogeneous rankings without relying on raw score scales |
| Cross-Encoder Reranking | Trade additional inference cost for stronger candidate relevance scoring |

See [`docs/decisions/`](docs/decisions/) for alternatives, trade-offs,
consequences, and validation strategies.
