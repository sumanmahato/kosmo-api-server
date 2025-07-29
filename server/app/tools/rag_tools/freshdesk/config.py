import os

# Freshdesk configuration
FRESHDESK_DOMAIN = os.environ.get("FRESHDESK_DOMAIN")  # e.g., "yourcompany.freshdesk.com"
FRESHDESK_API_KEY = os.environ.get("FRESHDESK_API_KEY")
FRESHDESK_KEY = "FRESHDESK"

# Caching and threading
FOLDER_CACHE_FILE = "freshdesk_folder_cache.json"
NUM_THREADS = 10
PER_PAGE = 100
FRESHDESK_FOLDER_CACHE_EXPIRY_HOURS = 24
