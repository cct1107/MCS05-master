import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 # $env:RAG_EMBED_MODEL="BAAI/bge-base-en-v1.5"
from extract_data.extract_from_pdf import extract_text_from_pdf
from extract_data.extract_from_url import extract_article_text
from extract_data.chunker import split_into_chunks_1, split_into_chunks_2, split_into_chunks_3, split_into_chunks_4, split_into_chunks_6
from process_dataset.build_dataset import build_and_save_index, build_and_save_bm25

if __name__ == "__main__":
    chunks = ["For individuals with prediabetes who are overweight or obese, a reduced calorie diet of 20–25 kcal per kilogram of body weight is recommended to achieve a weight loss of 5–10% of initial body weight within six months. To help manage blood sugar, carbohydrates should provide 45–60% of daily energy intake, protein 15–20%, and fat 25–35%. Saturated fat should be kept below 7% of total calories, and cholesterol intake should be less than 200 milligrams per day. A daily fiber intake of 20–30 grams is encouraged, while sodium should be limited to less than 2,400 milligrams per day."]

    # PDF
    # text = extract_text_from_pdf("backend/documents/factsheet_Prediabetes.pdf")
    # chunks += split_into_chunks_6(text)

    # # Web articles
    # urls = [
    #     "https://gleneagles.com.my/health-digest/prediabetes",
    #     "https://codeblue.galencentre.org/2025/05/one-in-10-people-with-prediabetes-are-likely-to-develop-type-2-diabetes-in-a-year/"
    # ]
    # for url in urls:
    #     text = extract_article_text(url)
    #     chunks += split_into_chunks_3(text)

    build_and_save_index(chunks, "faiss_index.index", "doc_store.json")
    build_and_save_bm25(chunks, "bm25.pkl")