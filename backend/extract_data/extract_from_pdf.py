import re
import fitz  

REFERENCE_HEADERS = re.compile(r'^\s*(references?|bibliography)\s*$', re.IGNORECASE)
SKIP_LINE_PATTERNS = [
    re.compile(r'^\s*copyright', re.IGNORECASE),
    re.compile(r'creative commons', re.IGNORECASE),
    re.compile(r'doi:\s*10\.\d{4,9}/\S+', re.IGNORECASE),
    re.compile(r'^https?://', re.IGNORECASE),
    re.compile(r'^\s*e-?mail|^\s*email', re.IGNORECASE),
    re.compile(r'^\s*correspondence', re.IGNORECASE),
    re.compile(r'^\s*received\s+\w+', re.IGNORECASE),
    re.compile(r'^\s*accepted\s+\w+', re.IGNORECASE),
    re.compile(r'^\s*published', re.IGNORECASE),
    re.compile(r'^\s*license', re.IGNORECASE),
]

def _looks_like_author_line(line: str) -> bool:

    parts = [p for p in line.split(',') if p.strip()]
    if len(parts) >= 2 and len(line) < 160 and line.count('.') <= 1:

        name_tokens = sum(bool(re.match(r'^[A-Z][a-zA-Z\-]+$', p.strip())) for p in parts)
        return name_tokens >= 2
    return False

def _is_junk(line: str) -> bool:
    l = line.strip()
    if not l:
        return True
    if len(l) < 3:
        return True
    if any(p.search(l) for p in SKIP_LINE_PATTERNS):
        return True
    if _looks_like_author_line(l):
        return True
    if l.isupper() and 3 <= len(l) <= 40:
        return True
    return False

def _normalize_hyphenation(text: str) -> str:
    return re.sub(r'(\w)-\n(\w)', r'\1\2', text)

def extract_text_from_pdf(file_path: str) -> str:

    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

def extract_clean_main_text(file_path: str) -> str:

    doc = fitz.open(file_path)
    collected = []
    in_references = False

    # Define vertical margins to ignore headers and footers
    # e.g., ignore top 10% and bottom 10% of the page
    TOP_MARGIN_RATIO = 0.10
    BOTTOM_MARGIN_RATIO = 0.90

    for page in doc:
        page_height = page.rect.height
        
        # Use sort=True to let PyMuPDF handle reading order
        blocks = page.get_text("blocks", sort=True)
        
        for b in blocks:  # b: (x0, y0, x1, y1, text, block_no, block_type)
            # Check if the block is within the vertical "safe zone"
            block_y0 = b[1]
            if block_y0 < page_height * TOP_MARGIN_RATIO or block_y0 > page_height * BOTTOM_MARGIN_RATIO:
                continue # Skip block if it's in the header or footer area

            raw = b[4]
            raw = _normalize_hyphenation(raw)
            lines = [l.strip() for l in raw.splitlines()]
            for line in lines:
                if not line:
                    continue
                if REFERENCE_HEADERS.match(line):
                    in_references = True
                    break
                if in_references:
                    continue
                if _is_junk(line):
                    continue
                collected.append(line)
        if in_references:
            break

    text = "\n".join(collected)
  
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()


if __name__ == "__main__":
    pdf_path = "backend/documents/International Journal of Endocrinology - 2013 - Hussein - Transcultural Diabetes Nutrition Algorithm  A Malaysian.pdf"
    main_text = extract_clean_main_text(pdf_path)
    print(main_text)
