import os
from typing import List, Sequence
from sentence_transformers import SentenceTransformer

MODEL_NAME = os.getenv("RAG_EMBED_MODEL", "BAAI/bge-base-en-v1.5")
model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts: Sequence[str]) -> List[List[float]]:
    vecs = model.encode(
        list(texts),
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return [v.tolist() for v in vecs]

def embed_chunk(text: str) -> List[float]:
    return embed_texts([text])[0]