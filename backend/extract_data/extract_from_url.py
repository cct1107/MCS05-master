import requests
from bs4 import BeautifulSoup

def extract_article_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    
    article = None
    if "codeblue.galencentre.org" in url:
        article = soup.find("div", class_="entry-content")
    elif "gleneagles.com.my" in url:
        article = soup.find("div", class_="content-section") or soup.find("div", class_="article-content")
    elif "webmd.com" in url:
        # Standard WebMD article
        article = (
            soup.find("div", class_="article-body")
            or soup.find("div", id="Article")
            or soup.find("div", id="main-content")
            or soup.find("div", class_="article__body")
            or soup.find("div", class_="article")
        )
        # Slideshow
        if not article:
            slides = soup.find_all("div", class_="slide")
            if slides:
                lines = []
                for slide in slides:
                    title = slide.find("h2") or slide.find("h3")
                    if title:
                        lines.append(f"\n### {title.get_text(strip=True)}")
                    for p in slide.find_all("p"):
                        lines.append(p.get_text(strip=True))
                return "\n".join(lines)
        # Blog
        if not article:
            article = soup.find("div", class_="blog-post__body")
    else:
        raise ValueError("Unsupported site structure")

    if not article:
        raise ValueError(f"Article content not found for {url}")

    lines = []
    for elem in article.find_all(["h1", "h2", "h3", "p", "ul", "ol", "strong"]):
        if elem.name in ["h1", "h2", "h3", "strong"]:
            lines.append(f"\n### {elem.get_text(strip=True)}")
        elif elem.name == "p":
            lines.append(elem.get_text(strip=True))
        elif elem.name in ["ul", "ol"]:
            for li in elem.find_all("li"):
                lines.append(f"- {li.get_text(strip=True)}")

    return "\n".join(lines)


if __name__ == "__main__":
    url_list = ["https://www.webmd.com/diabetes/stop-prediabetes-progression",
    "https://www.webmd.com/diabetes/diabetes-causes",
    "https://www.webmd.com/diabetes/ss/slideshow-prediabetes-diet",    
    "https://www.webmd.com/diet/glycemic-index-diet",
    "https://www.webmd.com/diabetes/ss/slideshow-snacks-blood-sugar",

        
        
        "https://www.webmd.com/diabetes/how-sugar-affects-diabetes",
        "https://www.webmd.com/diabetes/cm/t2d-reversed-remission",
        "https://blogs.webmd.com/diabetes/20240207/5-blood-sugar-friendly-swaps-for-valentines-day",
        "https://www.webmd.com/diet/glycemic-index-diet",
        "https://www.webmd.com/diabetes/glucose-diabetes",
        "https://www.webmd.com/diabetes/causes-blood-sugar-spikes",
        "https://www.webmd.com/diabetes/features/blood-sugar-level-older-adults",
        "https://www.webmd.com/diet/news/20240911/ultra-processed-doesnt-always-mean-bad-how-to-tell",
    
        "https://gleneagles.com.my/health-digest/prediabetes",
        "https://codeblue.galencentre.org/2025/05/one-in-10-people-with-prediabetes-are-likely-to-develop-type-2-diabetes-in-a-year/"
        ]
    text = ""
    chunks = []
    for url in url_list:
        text += extract_article_text(url)
        print(f"--- Content from {url} ---")
        print(text)
        print()

        from chunker import split_into_chunks_h3
        chunks += split_into_chunks_h3(text)
    for i, c in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(c)
        print()