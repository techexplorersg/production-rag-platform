from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def encode_documents(
        self,
        documents: List[str],
    ) -> np.ndarray:

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return np.asarray(
            embeddings,
            dtype="float32",
        )

    def encode_query(
        self,
        query: str,
    ) -> np.ndarray:

        embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return np.asarray(
            embedding,
            dtype="float32",
        )
