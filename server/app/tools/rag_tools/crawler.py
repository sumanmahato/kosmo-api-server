import asyncio
import os
import psutil
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, MemoryAdaptiveDispatcher

async def crawl_parallel(urls, max_concurrent=10):
    """
    Crawl multiple URLs in parallel and return a list of LangChain Documents.
    """
    print("\n=== Parallel Crawling with arun_many + Dispatcher ===")

    peak_memory = 0
    process = psutil.Process(os.getpid())

    def log_memory(prefix=""):
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
        results = await crawler.arun_many(urls=urls, config=crawl_config, dispatcher=dispatcher)

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


def extract_urls_from_sitemap(sitemap_url: str) -> list[str]:
    """
    Extract URLs from an XML sitemap.
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    response = requests.get(sitemap_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch sitemap: {sitemap_url} (status code {response.status_code})")

    soup = BeautifulSoup(response.text, 'xml')
    return [loc.text for loc in soup.find_all("loc")]


def is_text_based_url(url: str) -> bool:
    """
    Filter URLs to include only text-based content (ignore images, CSS, JS, etc.).
    """
    skip_exts = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".css", ".js",
                 ".woff", ".ttf", ".otf", ".eot", ".pdf"]
    return not any(url.lower().endswith(ext) for ext in skip_exts)
