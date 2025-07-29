import os
import time
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .api import fetch_freshdesk_api
from .config import FOLDER_CACHE_FILE, NUM_THREADS, FRESHDESK_FOLDER_CACHE_EXPIRY_HOURS

logger = logging.getLogger(__name__)

def fetch_categories():
    return fetch_freshdesk_api("/api/v2/solutions/categories") or []

def fetch_folders_for_category(category_id):
    return fetch_freshdesk_api(f"/api/v2/solutions/categories/{category_id}/folders") or []

def fetch_direct_subfolders(folder_id):
    endpoint = f"/api/v2/solutions/folders/{folder_id}/subfolders"
    return fetch_freshdesk_api(endpoint) or []

def get_all_folder_ids(use_cache=True, force_fetch=False):
    """Fetch and cache all Freshdesk folder IDs."""
    if use_cache and not force_fetch and os.path.exists(FOLDER_CACHE_FILE):
        try:
            cache_age = time.time() - os.path.getmtime(FOLDER_CACHE_FILE)
            if cache_age < FRESHDESK_FOLDER_CACHE_EXPIRY_HOURS * 3600:
                with open(FOLDER_CACHE_FILE, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error reading cache: {e}. Refetching.")

    logger.info("Fetching Freshdesk folders...")
    categories = fetch_categories()
    folder_ids = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = {executor.submit(fetch_folders_for_category, c["id"]): c["id"] for c in categories if "id" in c}
        for future in as_completed(futures):
            try:
                folders = future.result()
                if folders:
                    folder_ids.extend([f["id"] for f in folders if "id" in f])
            except Exception as e:
                logger.error(f"Error fetching folders: {e}")

    # Save cache
    try:
        with open(FOLDER_CACHE_FILE, "w") as f:
            json.dump(folder_ids, f)
    except Exception as e:
        logger.warning(f"Failed to write cache: {e}")

    return folder_ids
