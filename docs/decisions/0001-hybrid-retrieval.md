# ADR-001: Use Hybrid Retrieval

**Status:** Accepted

## Context

Dense retrieval provides semantic matching but may perform poorly when
queries depend on exact identifiers, acronyms, product names, or uncommon
technical terminology.

Lexical retrieval such as BM25 performs well for exact-token matching but
does not capture semantic similarity as effectively.

Using either independently creates different retrieval failure modes.

## Decision

Use two first-stage retrievers:

1. Dense retrieval using embeddings and FAISS
2. Lexical retrieval using BM25

Their candidate rankings are combined before reranking.

## Alternatives Considered

### Dense retrieval only

Advantages:
- Simple architecture
- Semantic matching

Disadvantages:
- Can miss exact terminology
- Embedding-model dependent

### BM25 only

Advantages:
- Fast
- Interpretable
- Strong exact-term matching

Disadvantages:
- Limited semantic understanding

## Consequences

Advantages:
- Better retrieval diversity
- Supports semantic and lexical matching
- Individual retrievers remain independently testable

Costs:
- Additional retrieval infrastructure
- More parameters to evaluate
- Increased observability requirements

## Validation

The architecture should be evaluated against a version-controlled golden
dataset using Recall@K, MRR, and Hit Rate@K rather than assuming hybrid
retrieval is automatically superior.
