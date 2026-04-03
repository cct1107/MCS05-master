from dotenv import load_dotenv
from google import genai
from typing import List
from google.genai.errors import ServerError
import time
import json
import re
import os

DETAIL_TRIGGER = re.compile(r'\b(detailed|detail|elaborate|explain in detail)\b', re.I)
MAX_WORDS_DEFAULT = 140
MAX_WORDS_EXTENDED = 260
load_dotenv()
google_client = google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
READABILITY_STYLE = (
    "Tone: warm, supportive, non-judgmental. Use simple everyday English, short sentences "
    "(~8–14 words), active voice. Avoid medical jargon unless necessary; if used, give a quick plain meaning. "
    "Do not lecture. Encourage small practical steps. End with a brief encouraging line (e.g., "
    "'Small consistent changes help.' or 'You’re on the right track.')."
)

def _sanitize_no_special(text: str) -> str:
    # Remove markdown bold/italics markers
    text = re.sub(r'[*_`]+', '', text)
    # Replace patterns like "GI 55 (low)" -> "GI 55 low"
    text = re.sub(r'\b(GI|Gl|GL)\s*([0-9]+)\s*\((low|medium|high|unknown)\)', r'\1 \2 \3', text, flags=re.I)
    # Remove standalone "(low)" etc.
    text = re.sub(r'\((low|medium|high|unknown)\)', r'\1', text, flags=re.I)
    # Collapse double spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def generate(query: str, rewrited_query, chunks: List[str], chunks_bm25: List[str], history: List[str], food_list: List[str]) -> str:
    wants_detail = bool(DETAIL_TRIGGER.search(query))
    max_words = MAX_WORDS_EXTENDED if wants_detail else MAX_WORDS_DEFAULT

    if food_list:
        food_block_rules = (
            "If foods are involved (explicitly named in user question/history):\n"
            "  1. Then one short summary sentence explaining why (e.g., presence of high-carb or high-GI foods).\n"
            "  2. Then line 'Tips:' followed by up to 3 concise, practical suggestions written as full sentences, NOT starting with '-'.\n"
            "  3. End with a short positive or encouraging sentence (e.g., 'Small consistent changes help.').\n"
            "Do NOT list each food separately and do NOT invent GI numbers.\n"
        )
    else:
        food_block_rules = (
            "User did NOT specify concrete foods. DO NOT output 'Overall risk:' line.\n"
            "Give: 1) One concise guidance sentence; 2) Up to 3 tips (portion, low GI pattern, plate balance) as full sentences, not starting with '-'; 3) Encouraging closing.\n"
            "Do NOT list specific food bullets or fabricate GI lines. No 'Overall risk'.\n"
        )

    format_rules = (
    f"{READABILITY_STYLE}\n"
    f"Word limit: {max_words} words (detail mode = {wants_detail}).\n"
    "NO special formatting: no *, **, tables, markdown headings, emojis, or parentheses ().\n"
    f"{food_block_rules}"
    "Do NOT mention or include any numeric GI or GL values, even if they are known or realistic.\n"
    "Instead, refer qualitatively (e.g., 'high GI', 'low GI', 'moderate GL') without numbers.\n"
    "Never output actual numeric values for GI or GL, even if they appear in the reference info.\n"
    "No parentheses for GI/GL classification. Only commas.\n"
    "Out-of-scope rule: if unrelated to prediabetes / blood sugar / GI / GL / carbs / metabolic lifestyle, output only:\n"
    "I am a prediabetes assistant. Please ask about prediabetes, blood sugar, GI/GL, diet, or related health topics.\n"
)

    prompt = f"""You are a prediabetes helper for Malaysian users.
        Answer the user's question in English only.

        {format_rules}

        User question (original):
        {query}
        User question (rewritten for context):
        {rewrited_query}

        Reference info (do NOT cite directly):
        {"\\n\\n".join(chunks)}

        Additional reference info (do NOT cite directly):
        {"\\n\\n".join(chunks_bm25)}

        Previous answer (for minimal context):
        {history[-1] if history else ""}

        Steps:
        1. Decide scope silently.
        2. If out-of-scope -> output scope message only.
        3. If in-scope -> follow required structure EXACTLY.
        4. No parentheses anywhere. No special formatting.
        5. No fabricated GI/GL numbers.
        6. Respect word limit.
        7. Sentences must be smooth, natural, and coherent for Malaysian English readers.
        8. Do NOT use bullet points (-). Sentences should be full, smooth, and connected. Keep all information from bullets, but merge into coherent paragraphs.
        """

    print(f"{prompt}\n---\n")
    delay = 2
    attempt = 0
    while attempt < 20:
        try:
            response = google_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw = response.text.strip()
            clean = _sanitize_no_special(raw)
            print(clean)
            return clean
        except ServerError as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(delay)
            delay += 2 + attempt
    return "I am a prediabetes assistant. Please ask about prediabetes, blood sugar, GI/GL, diet, or related health topics."




def rewrite_query_with_context_llm(history: List[str], query: str, is_detected: bool = False):
    """
    Rewrites the user query; returns (rewritten_query, food_list, portion_list, detected_food_list, is_prediabetes_related)
    food_list: list[str]
    portion_list: list[str]
    detected_food_list: list (already from detection pipeline if any)
    is_prediabetes_related: bool (True if query relates to prediabetes, blood sugar, GI/GL, or metabolic health)
    """
    context_text = " ".join(history) if history else ""

    prompt = f"""
    You are a query rewriter.
    Tasks:
    1. Fix grammar/spelling minimally.
    2. Make the query self-contained (resolve pronouns using history if needed).
    3. Do NOT invent new facts.
    4. If user mentions one or more foods, normalize each to a simple singular lowercase form
       (e.g., "White rice" -> "rice", "Boiled eggs" -> "egg").
    5. Portion extraction rule:
       - If the user mentions quantities (e.g., "100g rice", "two eggs"), extract them into a parallel list
         called PORTION_LIST, aligned by index with FOOD_LIST (e.g., ["rice","egg"], ["100","2"]).
       - If the portion is explicitly numeric (e.g., "100g"), use that value directly.
       - If the portion is described in words or countable units (e.g., "two eggs", "a bowl of rice", "one curry puff"),
         infer a reasonable approximate weight in grams based on general food knowledge.
       - If no portion or amount is given, use the default value "50".
       - The goal is to maintain internal consistency between foods and portions while keeping all portions in grams (g).
    6. Output strict JSON ONLY (no prose) with keys:
       RESULT        : rewritten question in English.
       FOOD_LIST     : array of zero or more normalized food names ([] if none).
       PORTION_LIST  : array of zero or more portion values (as strings, default "50" if unspecified).
       DETECTED_FOOD : list of detected food objects already known if is_detected is true 
                       (else []); DO NOT fabricate new foods. Keep it no matter what question the user asks.
        IS_PREDIABETES_RELATED : boolean; True if the user question is NOT about prediabetes, diabetes, blood sugar control, GI / GL,
            carbohydrate / nutrition, lifestyle changes related to metabolic / diabetes risk,
            detected food impact, or weight management for prediabetes. False otherwise.

    Rules:
        - If the user query contains a specific food item (e.g., nasi lemak, roti canai, laksa),
        reframe the RESULT (rewritten question) to focus on the food’s likely glycemic index (GI) category
        and general carbohydrate characteristics instead of the exact food name.
        However, DO NOT remove or alter FOOD_LIST or PORTION_LIST — they must still reflect the
        specific foods and their inferred portions from the user's original input.
        This ensures that even when the question is generalized for retrieval accuracy,
        the structured fields still preserve the user’s concrete input for downstream reasoning.

    Example:
        - "Can I eat nasi lemak?" → "Is it advisable for someone with prediabetes to eat high-GI foods such as white rice dishes?"
        - "What should I eat for breakfast?" → "What are some low-GI breakfast options suitable for people managing blood sugar?"
        - "Is oat porridge good for me?" → "Are low-GI foods such as oats recommended for people managing prediabetes?"
        - "I ate 100g of rice and one egg" → RESULT:"How do rice and egg affect blood sugar?", FOOD_LIST:["rice","egg"], PORTION_LIST:["100","50"], IS_PREDIABETES_RELATED:true
        - "What is the capital of Malaysia?" → IS_PREDIABETES_RELATED:false

    Additional constraints:
    - sugar-free foods / sugar-free drink is NOT a food name (ignore).
    - Never merge multiple foods into one string; always separate list items.
    - Return ONLY JSON. No markdown, no commentary.

    Conversation history:
    {context_text}

    User query:
    {query}

    is_detected:
    {is_detected}

    Valid JSON examples:
    {{"RESULT":"What is the glycemic impact of eating rice and egg together?","FOOD_LIST":["rice","egg"],"PORTION_LIST":["50","50"],"DETECTED_FOOD":[],"IS_PREDIABETES_RELATED":true}}
    {{"RESULT":"How does rice affect blood sugar?","FOOD_LIST":["rice"],"PORTION_LIST":["50"],"DETECTED_FOOD":[],"IS_PREDIABETES_RELATED":true}}
    {{"RESULT":"What are lifestyle changes to lower prediabetes risk?","FOOD_LIST":[],"PORTION_LIST":[],"DETECTED_FOOD":[],"IS_PREDIABETES_RELATED":true}}
    {{"RESULT":"Who is the prime minister of Malaysia?","FOOD_LIST":[],"PORTION_LIST":[],"DETECTED_FOOD":[],"IS_PREDIABETES_RELATED":false}}

    Return JSON only:
    """

    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    raw_text = response.text.strip()
    result = safe_json_extract(raw_text)

    rewritten_query = result.get("RESULT", query)

    # --- Extract FOOD_LIST safely ---
    food_list = result.get("FOOD_LIST", [])
    if isinstance(food_list, str):
        parts = re.split(r'\s*(?:,|&| and )\s*', food_list.strip())
        food_list = [p for p in parts if p]
    if not isinstance(food_list, list):
        food_list = []
    food_list = [f.strip().lower() for f in food_list if isinstance(f, str) and f.strip() and "sugar-free" not in f.lower()]

    # --- Extract PORTION_LIST safely ---
    portion_list = result.get("PORTION_LIST", [])
    if isinstance(portion_list, str):
        portion_list = [portion_list]
    if not isinstance(portion_list, list):
        portion_list = []
    portion_list = [p.strip().lower() for p in portion_list if isinstance(p, str) and p.strip()]

    # --- Keep DETECTED_FOOD as is ---
    detected_food = result.get("DETECTED_FOOD", [])

    # --- Determine if the question relates to prediabetes or not ---
    is_prediabetes_related = result.get("IS_PREDIABETES_RELATED", False)
    if isinstance(is_prediabetes_related, str):
        is_prediabetes_related = is_prediabetes_related.lower() in ("true", "yes", "1")

    print("Rewritten Query:", rewritten_query)
    print("Food List:", food_list)
    print("Portion List:", portion_list)
    print("Prediabetes Related:", is_prediabetes_related)

    return rewritten_query, food_list, portion_list, detected_food, is_prediabetes_related


def safe_json_extract(raw_text: str) -> dict:
    cleaned = re.sub(r'^[`\s"]*json', '', raw_text.strip(), flags=re.IGNORECASE).strip()
    cleaned = cleaned.strip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON, raw output:", raw_text)
        return {"RESULT": "", "FOOD_LIST": [], "DETECTED_FOOD": []}


def weekly_tip(context: str) -> str:
    prompt = (
        "You are a prediabetes assistant. Generate a brief, friendly, practical weekly tip for Malaysian users with prediabetes. "
        "The tip should be about diet, lifestyle, or blood sugar management. "
        "Use simple English, short sentences, and a warm tone. "
        "Limit to 150 words. No special formatting or punctuation."
    )
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
    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt + "\n\nContext:\n" + context + "\n\n" + GL_GUIDE
    )
    raw = response.text.strip()
    clean = _sanitize_no_special(raw)
    print("Weekly Tip:", clean)
    return clean


def process_meal(meal: dict) -> list:
    description = meal.get("description", "")
    nutrition_info = meal.get("nutrition_info", [])

    prompt = ( 
        "Given the following meal description and detected nutrition info, " 
        "for foods already present in the nutrition info, you may ONLY change the portion value; " 
        "do NOT change name, gi, gl, or carbohydrate for existing foods. " 
        "If a specific amount is mentioned, adjust the portion. " 
        "If 50g per serving seems unrealistically small based on the context, estimate a reasonable portion. " 
         "Typical Malaysian food portions (grams): "
            "A bowl of rice ≈ 150g, "
            "One curry puff ≈ 60g, "
            "One Char Kuey Teow ≈ 350g, "
            "One Kuih Lapis ≈ 40g, "
            "One Singgang ikan ≈ 120g, "
            "One Solok lada ≈ 80g. "
        "Also, add any missing foods with estimated GI/GL/carbohydrate values if possible. " 
        "Return the result as a JSON list. " 
        "Do NOT use keys like 'food_item', 'portion_g', 'estimated_gi', etc. " 
        "Always use this exact format:\n" 
        "[\n" 
        " {\n" 
            " \"name\": \"Rice\",\n" 
            " \"gi\": \"73\",\n" 
            " \"gl\": \"33\",\n" 
            " \"carbohydrate\": \"45\",\n" 
            " \"portion\": 150\n" " },\n" 
            " ...\n" 
        "]\n" 
        "Return ONLY the JSON list, no explanation or extra text.\n" 
        f"\nDescription: {description}\n" 
        f"Nutrition Info: {nutrition_info}\n" 
        "IMPORTANT: Do NOT fabricate GI/GL/carbohydrate values for existing foods. "
        "You may only add new foods if they are clearly implied by the description. "
    )

    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    ai_result = response.text.strip()
    print("AI Nutrition Info Output:", ai_result)

    try:
        json_str = extract_json(ai_result)
        raw_nutrition_info = json.loads(json_str)
        if isinstance(raw_nutrition_info, dict):
            raw_nutrition_info = [raw_nutrition_info]
        if not isinstance(raw_nutrition_info, list):
            raw_nutrition_info = nutrition_info
        cleaned = clean_nutrition_info(raw_nutrition_info)
    except Exception as e:
        print("⚠️ Failed to parse AI nutrition_info, fallback to original.", e)
        cleaned = clean_nutrition_info(nutrition_info)
    return cleaned

def clean_nutrition_info(nutrition_info):
    merged = {}
    for food in nutrition_info:
        key = normalize_name(food.get("name", ""))
        if not key:
            continue
        gi = parse_number(food.get("gi", 0))
        gl = parse_number(food.get("gl", 0))
        carb = parse_number(food.get("carbohydrate", 0))
        portion = parse_number(food.get("portion", 100))
        if key in merged:
            merged[key]["gi"] = (merged[key]["gi"] + gi) / 2
            merged[key]["gl"] = (merged[key]["gl"] + gl) / 2
            merged[key]["carbohydrate"] = (merged[key]["carbohydrate"] + carb) / 2
            merged[key]["portion"] = (merged[key]["portion"] + portion) / 2
        else:
            merged[key] = {
                "name": food.get("name", ""),
                "gi": gi,
                "gl": gl,
                "carbohydrate": carb,
                "portion": portion
            }
    return list(merged.values())

def parse_number(val):
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        parts = val.replace(' ', '').split('-')
        try:
            nums = [float(p) for p in parts if p]
            if len(nums) == 1:
                return nums[0]
            elif len(nums) == 2:
                return sum(nums) / 2
        except Exception:
            pass
    return 0.0

def normalize_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def extract_json(text):
    cleaned = re.sub(r'^[`\s"]*json', '', text.strip(), flags=re.IGNORECASE).strip()
    cleaned = cleaned.strip('`').strip()
    match = re.search(r'\[.*\]', cleaned, re.DOTALL)
    if match:
        return match.group(0)
    return cleaned


def individual_food_analysis(food: dict, description: str) -> dict:
    name = food.get("name", "food item")
    gi = food.get("gi", "unknown")
    gl = food.get("gl", "unknown")
    carb = food.get("carbohydrate", "unknown")
    portion = food.get("portion", "100")
    nutrition_info = food.get("nutrition_info", {})

    prompt = (
        f"Use simple English and a warm, supportive tone. "
        f"Limit to 100 words. No special formatting or punctuation.\n\n"
        f"Food item details:\n"
        f"Name: {name}\n"
        f"GI: {gi}\n"
        f"GL: {gl} (based on 100 g)\n"
        f"Carbohydrate (g): {carb}\n"
        f"Portion (g): {portion} (all ready consider the number of servings)\n"
        f"Additional nutrition info: {nutrition_info}\n"
        f"Description/context: {description}\n\n"
        "First, give a one-word rating for this food's suitability for prediabetes: "
        "Rating: poor, average, or good (based on qualitative understanding of GL — good means lower impact, poor means higher impact). "
        "Do NOT mention or include any numeric GI or GL values. Only use qualitative words such as 'low GI', 'high GI', or 'moderate GL'. "
        "Then, explain your reasoning in 1–2 sentences. "
        "Then, give a practical tip or substitution if needed. "
        "Format:\n"
        "Rating: [poor|average|good]\n"
        "Reason: ...\n"
        "Tip: ...\n"
        "IMPORTANT: Your answer MUST include all three lines: 'Rating:', 'Reason:', and 'Tip:'. "
        "If any line is missing, your answer is not valid. Do not add any extra lines or explanation. "
        "Never mention or display numeric GI, GL, or carbohydrate values in the response."
    )

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

    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt + "\n\n" + GL_GUIDE
    )
    raw = response.text.strip()
    clean = _sanitize_no_special(raw)
    rating, reason, tip, text = extract_rating_and_text(clean)

    print(f"Food Analysis for {name}:\n", rating, "\n", text)
    return {"rating": rating, "reason": reason, "tip": tip, "analysis": text}

def extract_rating_and_text(ai_text):
    rating = "unknown"
    reason = ""
    tip = ""
    match = re.search(r'Rating:\s*(poor|average|good)', ai_text, re.IGNORECASE)
    if match:
        rating = match.group(1).lower()
    match_reason = re.search(r'Reason:\s*(.*?)(?:\n|$)', ai_text, re.IGNORECASE)
    if match_reason:
        reason = match_reason.group(1).strip()
    match_tip = re.search(r'Tip:\s*(.*?)(?:\n|$)', ai_text, re.IGNORECASE)
    if match_tip:
        tip = match_tip.group(1).strip()
    return rating, reason, tip, ai_text