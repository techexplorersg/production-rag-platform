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
