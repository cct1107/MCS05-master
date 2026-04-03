import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from search_data.retrieve_food_information import get_food_information
from search_data.retrieve import retrieve, bm25_retrieve
from process_dataset.build_dataset import load_index_and_docs, load_bm25
from search_data.rerank import rerank
from generate_answer.generate import generate, rewrite_query_with_context_llm
# from bm25_retrieve import BM25Retriever
FYP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONVERSATION_HISTORY = []

def rewrite_query_with_context(history: List[str], query: str) -> str:

    if not history:
        return query
    context_text = " ".join(history[-2:]) 
    rewritten = f"{context_text} {query}"
    return rewritten

def query_pipeline(query: str, is_detected: bool = False) -> str:
    # index, doc_store = load_index_and_docs(
    # r"C:\Users\User\Desktop\FYP\faiss_index.index",
    # r"C:\Users\User\Desktop\FYP\doc_store.json"
    # )
    # bm25 = load_bm25("bm25.pkl")
    print("+++++++++++++++++++++++++++++")
    print("User query:", query)
    print("Is detected:", is_detected)
    print("+++++++++++++++++++++++++++++")
    index, doc_store = load_index_and_docs(
        os.path.join(FYP_ROOT, "faiss_index.index"),
        os.path.join(FYP_ROOT, "doc_store.json"),
    )
    bm25 = load_bm25(os.path.join(FYP_ROOT, "bm25.pkl"))
    history = CONVERSATION_HISTORY[-2:]
    rewritten_query, food_list, portion_list, detected_food, is_prediabetes_related = rewrite_query_with_context_llm(history, query, is_detected)
    if not is_prediabetes_related:
        history.append(f"User: {query}")
        history.append("Bot: I am a prediabetes assistant. Please ask about prediabetes, blood sugar, GI/GL, diet, or related health topics.")
        return "I am a prediabetes assistant. Please ask about prediabetes, blood sugar, GI/GL, diet, or related health topics."
    # index, doc_store = load_index_and_docs("faiss_index.index", "doc_store.json")
    # add llm ()
    retrieved_chunks = retrieve(rewritten_query, index, doc_store, top_k=10)
    reranked_chunks = rerank(rewritten_query, retrieved_chunks, top_k=4)
    bm25_results = bm25_retrieve(rewritten_query, bm25, doc_store, top_k=4)

    # Remove duplicates from bm25_results that are already in reranked_chunks
    reranked_contents = set(reranked_chunks)
    unique_bm25_results = [chunk for chunk in bm25_results if chunk not in reranked_contents]


    print(food_list)
    GL_GUIDE = (
    "GL/GI quick guide. "
    "Glycemic Load (GL) reflects both food type and portion — it shows how much a serving will raise blood sugar. "
    "Glycemic Index (GI) shows how fast carbs turn into glucose, but not how much you eat. "
    "GL bands per serving: Low ≤10, Medium 11–19, High ≥20. "
    "GI categories: Low ≤55, Medium 56–69, High ≥70. "
    "Formula: GL = GI × available carbs (g) ÷ 100. "
    
    "Examples — "
    "Low-GL: small serve of brown or mixed rice, oats, dhal/lentils, chapati, most fruits (guava, papaya, apple), "
    "non-starchy vegetables (kangkong, sawi, cabbage), tofu, nuts. "
    "Medium-GL: moderate serve of brown rice or mee goreng (not too oily/sweet), corn, banana (moderately ripe), "
    "some nasi lemak with limited rice and sambal. "
    "High-GL: white rice (large portion), bihun (rice vermicelli), roti canai, pulut (glutinous rice), "
    "kuih manis (sweet coconut desserts), nasi lemak with lots of sambal and coconut milk, "
    "sweet drinks (teh tarik, sirap bandung, condensed-milk drinks). "
    
    "Proteins (egg, fish, chicken, tofu) have negligible GL unless deep-fried or coated with high-carb batter or sauce. "
    "Fats and oils also have no GI/GL but can raise calories. "
    
    "Lower-GL tips: "
    "reduce rice/noodle portion, replace white rice with brown or mixed rice, "
    "add vegetables and protein (fish, egg, tofu, dhal), "
    "limit sambal, coconut milk, and sweet sauces, "
    "avoid sugary drinks and kuih as regular snacks. "
    
    "When answering: classify foods mainly by GL based on typical Malaysian portion, "
    "mention GI only if useful for comparison, flag high-GL risks for prediabetes, "
    "and give short, practical substitution or portion advice (e.g. 'half-plate rice, add veg + tofu')."
)
    combined_info_texts = []
    index = 0
    if food_list:
        
        for food in food_list:
            try:
                food_info_df = get_food_information(food)
                if not food_info_df.empty:
                    combined_info_texts.append(f"Food '{food}': {food_info_df} portion {portion_list[index] if index < len(portion_list) else '50'}g.")
            except Exception as e:
                print(f"[food_info] Error for {food}: {e}")

    print("########################\n result: ", bm25_results, "\n########################")
    if combined_info_texts:
            rewritten_query += (
                ". The following food details are provided:\n" +
                "\n".join(combined_info_texts)
            )

    if detected_food:
        rewritten_query += f". The detected foods in the image are: {detected_food}. "
        rewritten_query += "Use the provided GI, GL, and carbohydrate values directly (do not generate or assume new numbers). "
    print("Detected food information added to the query:", detected_food)

    if combined_info_texts or detected_food:
        rewritten_query += " Also, use the GL/GI quick guide below to inform your answer:\n" + GL_GUIDE

    answer = generate(query, rewritten_query, reranked_chunks, unique_bm25_results, history, detected_food + food_list)

    CONVERSATION_HISTORY.append(f"User: {query}")
    CONVERSATION_HISTORY.append(f"Bot: {answer}")
    return answer


if __name__ == "__main__":
    "What are the symptoms of prediabetes?"
    query = "I am 40 years old and I want to know can I drink coffee?"

    answer = query_pipeline(query)

    print("Answer:")
    print(answer)