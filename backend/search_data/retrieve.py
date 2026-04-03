from rpds import List
from textblob import Word
import numpy as np
from typing import List
from process_dataset.embedding import embed_chunk
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

def correct_query(query: str) -> str:

    words = query.split()
    corrected_words = []
    for w in words:
        if w.lower() not in STOPWORDS and w.isalpha():
            corrected_words.append(str(Word(w).correct()))
        else:
            corrected_words.append(w)
    return " ".join(corrected_words)

def retrieve(query: str, index, doc_store: List[str], top_k: int = 10) -> List[str]:
    query = correct_query(query)
    query_embedding = np.array([embed_chunk(query)]).astype("float32")
    distances, indices = index.search(query_embedding, top_k * 2) 

    retrieved = [doc_store[i] for i in indices[0]]


    seen = set()
    unique_chunks = []
    for chunk in retrieved:
        normalized = chunk.lower().strip()  
        if normalized not in seen:
            seen.add(normalized)
            unique_chunks.append(chunk)
        if len(unique_chunks) == top_k: 
            break


    if len(unique_chunks) < top_k:
        for chunk in retrieved:
            if chunk not in unique_chunks:
                unique_chunks.append(chunk)
            if len(unique_chunks) == top_k:
                break

    return unique_chunks

def embedding_search(query: str, index, doc_store: List[str], top_k: int = 5) -> List[str]:
    query_embedding = np.array([embed_chunk(query)]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    return [doc_store[i] for i in indices[0]]

def keyword_search(query: str, bm25: BM25Okapi, doc_store: List[str], top_k: int = 5) -> List[str]:
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [doc_store[i] for i in top_indices]

def hybrid_retrieve(query: str, index, bm25: BM25Okapi, doc_store: List[str], top_k: int = 5) -> List[str]:
    emb_results = embedding_search(query, index, doc_store, top_k)
    kw_results = keyword_search(query, bm25, doc_store, top_k)

    combined = list(set(emb_results + kw_results))

    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = [(query, chunk) for chunk in combined]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(combined, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scored_chunks][:top_k]

def bm25_retrieve(query: str, bm25: BM25Okapi, doc_store: List[str], top_k: int = 5) -> List[str]:
    # query = correct_query(query)
    # print("Corrected query:", query)
    tokenized_query = [word for word in query.lower().split() if word not in STOPWORDS]

    if not tokenized_query:
        tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [doc_store[i] for i in top_indices]