from app.ingestion.chunker import RecursiveTextChunker


def test_chunker_creates_multiple_chunks():

    text = (
        "Machine learning systems require monitoring. "
        "Production systems require observability. "
        "Retrieval systems require evaluation. "
    ) * 20

    chunker = RecursiveTextChunker(
        chunk_size=200,
        chunk_overlap=30,
    )

    chunks = chunker.split(
        document_id="test-doc",
        text=text,
    )

    assert len(chunks) > 1

    assert all(
        chunk.document_id == "test-doc"
        for chunk in chunks
    )

    assert all(
        len(chunk.text) > 0
        for chunk in chunks
    )
