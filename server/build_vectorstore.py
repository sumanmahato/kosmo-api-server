import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from app.tools.rag_tools.crawler import extract_urls_from_sitemap, is_text_based_url, crawl_parallel
from app.tools.rag_tools.vectorstore import embed_documents_to_chroma

def build_vectorstore_from_sitemap(sitemap_url, persist_dir="chroma_db"):
    print(f"[INFO] Building vectorstore from sitemap: {sitemap_url}")
    os.makedirs(persist_dir, exist_ok=True)

    all_urls = extract_urls_from_sitemap(sitemap_url)
    print(f"[INFO] Found {len(all_urls)} total URLs in sitemap")

    urls = [url for url in all_urls if is_text_based_url(url)]
    print(f"[INFO] Filtered down to {len(urls)} crawlable text URLs")

    try:
        documents = asyncio.run(crawl_parallel(urls, max_concurrent=10))
    except Exception as e:
        print(f"[ERROR] Crawling failed: {e}")
        return

    if not documents:
        print("[ERROR] No content crawled from sitemap")
        return

    embed_documents_to_chroma(documents, persist_dir)
    print(f"[INFO] Vectorstore build complete at '{persist_dir}'")

if __name__ == "__main__":
    build_vectorstore_from_sitemap("https://www.komprise.com/post-sitemap1.xml")
