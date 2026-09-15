from dataclasses import dataclass
from typing import List


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    start: int
    end: int


class RecursiveTextChunker:
    """
    Lightweight recursive-style text chunker.

    Keeps overlap between adjacent chunks so retrieval does not lose
    information that falls across chunk boundaries.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 120,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
        self,
        document_id: str,
        text: str,
    ) -> List[Chunk]:

        text = text.strip()

        if not text:
            return []

        chunks = []

        start = 0
        chunk_number = 0

        while start < len(text):

            end = min(
                start + self.chunk_size,
                len(text),
            )

            # Try to avoid splitting in the middle of a sentence.
            if end < len(text):
                sentence_boundary = text.rfind(
                    ". ",
                    start,
                    end,
                )

                if sentence_boundary > start:
                    end = sentence_boundary + 1

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    Chunk(
                        chunk_id=f"{document_id}-{chunk_number}",
                        document_id=document_id,
                        text=chunk_text,
                        start=start,
                        end=end,
                    )
                )

                chunk_number += 1

            if end >= len(text):
                break

            start = max(
                end - self.chunk_overlap,
                start + 1,
            )

        return chunks
