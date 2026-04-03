import re
import spacy
from sentence_transformers import SentenceTransformer, util
from typing import List

nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2") 

def split_into_chunks_1(text: str, max_length: int = 500) -> List[str]:

    sentences = re.split(r'(?<=[。！？!.?])\s+', text)
    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_length:
            chunk += sentence + " "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
    if chunk:
        chunks.append(chunk.strip())

    # filtered_chunks = [chunk for chunk in chunks if len(chunk.strip()) > 30]
    # return filtered_chunks
    return chunks

def split_into_chunks_2(text: str, max_length: int = 500) -> list:
    
    sentences = text.split("\n\n")
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < max_length:
            chunk += sentence + "\n\n"
        else:
            chunks.append(chunk.strip())
            chunk =sentence + "\n\n"
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def split_into_chunks_3(text: str) -> List[str]:

    sentences = re.split(r'(?<=[。！？!.?])\s+', text)
    return [s for s in sentences if s.strip()]

def split_into_chunks_4(text: str) -> List[str]:

    sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])', text)
    chunks = []
    current_question = ""
    current_answer = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if sentence.endswith("?"):
            if current_question:
                chunks.append(f"{current_question} {current_answer}".strip())
                current_answer = ""
            current_question = sentence
        else:
            current_answer += sentence + " "

    if current_question:
        chunks.append(f"{current_question} {current_answer}".strip())

    return chunks

def split_into_chunks_5(text: str) -> List[str]:

    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    buffer = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        buffer += sentence + " "

        if sentence.endswith("."):
            chunks.append(buffer.strip())
            buffer = ""

    if buffer:
        chunks.append(buffer.strip())

    return chunks

import re

def is_reference_like(sentence: str) -> bool:
    patterns = [
        r"\(\d{4}\)",   
        r"\bdoi\b",     
        r"[A-Z]\w*\.",  
        r"\d+,\s*\d+"   
    ]
    return any(re.search(p, sentence) for p in patterns)

def is_too_short(sentence: str, min_chars: int = 50, min_words: int = 5) -> bool:
    return len(sentence) < min_chars or len(sentence.split()) < min_words

def clean_text(text: str) -> str:
    """
    Clean the text by removing control characters and unnecessary symbols,
    while keeping important punctuation like ., ?, !
    """

    text = re.sub(r'[\u0000-\u001F\u007F]', ' ', text)

    text = re.sub(r'[•▪–—]', ' - ', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def split_into_chunks_6(text, similarity_threshold=0.7, max_chunk_size=1500):

    doc = nlp(text)
    sentences = [
        clean_text(sent.text)
        for sent in doc.sents
        if sent.text.strip()
        and not is_too_short(sent.text.strip())
        and not is_reference_like(sent.text.strip())
    ]

    if not sentences:
        return []

    embeddings = embedder.encode(sentences, convert_to_tensor=True)

    chunks = []
    current_chunk = sentences[0]
    current_embedding = embeddings[0]

    for i in range(1, len(sentences)):
        similarity = util.cos_sim(current_embedding, embeddings[i]).item()

        if similarity > similarity_threshold and len(current_chunk) + len(sentences[i]) < max_chunk_size:
            current_chunk += " " + sentences[i]
            current_embedding = (current_embedding + embeddings[i]) / 2
        else:
            if len(current_chunk.strip()) > 15 and not is_reference_like(current_chunk):
                chunks.append(current_chunk.strip())
            current_chunk = sentences[i]
            current_embedding = embeddings[i]

    if current_chunk and len(current_chunk.strip()) > 15 and not is_reference_like(current_chunk):
        chunks.append(current_chunk.strip())

    return chunks

def split_into_chunks_h3(text: str,
                         keep_hashes: bool = False,
                         min_body_chars: int = 80,
                         min_body_words: int = 10,
                         join_with_space: bool = True) -> List[str]:
    """
    Split text by '### ' headings.
    Each chunk = heading + its body (until next '### ' or end).
    Discard chunks whose body is too short (both char and word thresholds).
    
    Args:
        keep_hashes: keep the leading '### ' in heading.
        min_body_chars: minimum body character length to keep a chunk.
        min_body_words: minimum body word count to keep a chunk.
    Notes:
        Text before the first '### ' is ignored.
    """
    lines = text.splitlines()
    sections: List[str] = []
    current_title = None
    current_buffer: List[str] = []

    def flush():
        if current_title is None:
            return
        body = " ".join(current_buffer).strip()
        body = re.sub(r'\s+', ' ', body)
        if not body:
            return
        body_words = len(re.findall(r'\w+', body))
        if len(body) < min_body_chars or body_words < min_body_words:
            return
        if keep_hashes:
            chunk_title = current_title
        else:
            chunk_title = re.sub(r'^###\s*', '', current_title).strip()
        sep = " " if join_with_space else "\n"
        sections.append(f"{chunk_title}{sep}{body}")

    for line in lines:
        if line.startswith("### "):
            flush()
            current_title = line.strip()
            current_buffer = []
        else:
            if current_title is not None:
                current_buffer.append(line)

    flush()
    return sections