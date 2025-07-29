import time
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .api import fetch_freshdesk_api
from .folders import get_all_folder_ids
from .config import PER_PAGE, NUM_THREADS, FRESHDESK_DOMAIN, FRESHDESK_KEY

logger = logging.getLogger(__name__)

def fetch_articles_page(folder_id, page=1):
    return fetch_freshdesk_api(
        f"/api/v2/solutions/folders/{folder_id}/articles",
        params={"page": page, "per_page": PER_PAGE}
    )

def fetch_articles_for_folder(folder_id):
    page = 1
    articles = []
    while True:
        page_data = fetch_articles_page(folder_id, page)
        if not page_data:
            break
        articles.extend(page_data)
        if len(page_data) < PER_PAGE:
            break
        page += 1
        time.sleep(0.1)
    return articles

def fetch_all_articles(force_fetch=False):
    folder_ids = get_all_folder_ids(force_fetch=force_fetch)
    all_articles = []
    with tqdm(total=len(folder_ids), desc="Fetching Articles", ncols=100) as pbar:
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {executor.submit(fetch_articles_for_folder, fid): fid for fid in folder_ids}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_articles.extend(result)
                pbar.update(1)
    return all_articles

def preprocess_articles(articles):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = []
    for article in articles:
        aid = str(article.get("id"))
        title = article.get("title", "No Title")
        content = article.get("description", "")
        if not aid or not title or not content:
            continue
        plain_text = BeautifulSoup(content, "html.parser").get_text()
        full_text = f"{title}\n\n{plain_text}"
        chunks = splitter.split_text(full_text)
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"{FRESHDESK_KEY}_{aid}_chunk_{i}",
                "text": chunk,
                "metadata": {
                    "title": title,
                    "url": f"https://{FRESHDESK_DOMAIN}/support/solutions/articles/{aid}",
                    "tags": article.get("tags", []),
                    "created_at": article.get("created_at"),
                    "updated_at": article.get("updated_at")
                }
            })
    return docs
