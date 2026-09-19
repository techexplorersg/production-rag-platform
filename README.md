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
