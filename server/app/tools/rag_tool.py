from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.models.embedding_wrapper import get_embedding_model

from tqdm import tqdm
import asyncio
import os
import psutil
import requests

from typing import List, Dict, Any
from urllib.parse import urlparse, urldefrag
from xml.etree import ElementTree

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    MemoryAdaptiveDispatcher
)

from bs4 import BeautifulSoup

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.config import Settings
import chromadb


# Optional: Configure via env
CHROMA_DB_DIR = "chroma_db"
EMBED_MODEL = "nomic-embed-text"

async def crawl_parallel(urls: List[str], max_concurrent: int = 10) -> List[Document]:
    print("\n=== Parallel Crawling with arun_many + Dispatcher ===")

    peak_memory = 0
    process = psutil.Process(os.getpid())

    def log_memory(prefix: str = ""):
        nonlocal peak_memory
        current_mem = process.memory_info().rss
        if current_mem > peak_memory:
            peak_memory = current_mem
        print(f"{prefix} Current Memory: {current_mem // (1024 * 1024)} MB, Peak: {peak_memory // (1024 * 1024)} MB")

    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=False)
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=max_concurrent
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        log_memory("Before crawl: ")

        results = await crawler.arun_many(
            urls=urls,
            config=crawl_config,
            dispatcher=dispatcher
        )

        documents = []
        for result in results:
            if result.success and result.markdown:
                documents.append(Document(page_content=result.markdown, metadata={"source": result.url}))
                print(f"[OK] {result.url}")
            else:
                print(f"[FAIL] {result.url}: {result.error_message}")

        log_memory("After crawl: ")
        print(f"\n✅ Successfully crawled: {len(documents)} / {len(urls)}")
        return documents
    
def embed_documents_to_chroma(documents, persist_dir="chroma_db", batch_size=64):
    print("[INFO] Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)
    print(f"[INFO] Split into {len(split_docs)} chunks.")

    embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    chroma_client = chromadb.Client(Settings(persist_directory=persist_dir))
    collection = chroma_client.get_or_create_collection(
        name="website_crawl",
        embedding_function=embedding_fn
    )

    print("[INFO] Adding documents to ChromaDB collection in batches...")

    # Batching logic
    for i in tqdm(range(0, len(split_docs), batch_size), desc="Embedding docs"):
        batch = split_docs[i:i+batch_size]

        batch_documents = [doc.page_content for doc in batch]
        batch_ids = [f"doc-{i + j}" for j in range(len(batch))]
        batch_metadatas = [doc.metadata for doc in batch]

        try:
            collection.add(
                documents=batch_documents,
                ids=batch_ids,
                metadatas=batch_metadatas
            )
        except Exception as e:
            print(f"[WARN] Failed to add batch {i}-{i + len(batch) - 1}: {e}")

    print(f"[INFO] Successfully added {len(split_docs)} documents to {persist_dir}.")
    print("[INFO] Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)
    print(f"[INFO] Split into {len(split_docs)} chunks.")

    embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # Create Chroma client with persistence
    chroma_client = chromadb.Client(Settings(persist_directory=persist_dir))
    collection = chroma_client.get_or_create_collection(
        name="website_crawl",
        embedding_function=embedding_fn
    )

    print("[INFO] collection done")

    print("[INFO] Adding documents to ChromaDB collection...")
    for i, doc in enumerate(tqdm(split_docs, desc="Embedding docs")):
        try:
            collection.add(
                documents=[doc.page_content],
                ids=[f"doc-{i}"],
                metadatas=[doc.metadata]
            )
        except Exception as e:
            print(f"[WARN] Failed to add doc-{i}: {e}")

    print(f"[INFO] Successfully added {len(split_docs)} documents to {persist_dir}. Data is auto-persisted.")

def extract_urls_from_sitemap(sitemap_url: str) -> list[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    response = requests.get(sitemap_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch sitemap: {sitemap_url} (status code {response.status_code})")

    soup = BeautifulSoup(response.text, 'xml')
    return [loc.text for loc in soup.find_all("loc")]

def is_text_based_url(url: str) -> bool:
    # Reject URLs ending in binary extensions
    skip_exts = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".css", ".js", ".woff", ".ttf", ".otf", ".eot", ".pdf"]
    return not any(url.lower().endswith(ext) for ext in skip_exts)

def build_vectorstore_from_sitemap(sitemap_url: str, persist_dir: str = "chroma_db"):
    all_urls = extract_urls_from_sitemap(sitemap_url)
    print(f"[INFO] Found {len(all_urls)} total URLs in sitemap")

    # Filter only text/html content URLs
    urls = [url for url in all_urls if is_text_based_url(url)]
    print(f"[INFO] Filtered down to {len(urls)} crawlable text URLs")

    documents = asyncio.run(crawl_parallel(urls, max_concurrent=10))
    if not documents:
        print("[ERROR] No content crawled from sitemap")
        return

    embed_documents_to_chroma(documents, persist_dir)

def load_existing_vectorstore(persist_dir: str = CHROMA_DB_DIR, embed_model: str = EMBED_MODEL):
    """
    Load an existing Chroma vectorstore for retrieval.
    """
    embeddings = get_embedding_model(embed_model)
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    print(f"[INFO] Loaded existing vectorstore from '{persist_dir}'")
    return vectorstore
