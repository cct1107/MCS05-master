from rank_bm25 import BM25Okapi
from typing import List

class BM25Retriever:
    def __init__(self, chunks: List[str]):
        
        self.tokenized_corpus = [chunk.split() for chunk in chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.chunks = chunks

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.chunks[i] for i in ranked_indices], [scores[i] for i in ranked_indices]
