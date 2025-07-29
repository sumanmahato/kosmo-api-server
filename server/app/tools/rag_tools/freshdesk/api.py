import requests
import logging
from .config import FRESHDESK_DOMAIN, FRESHDESK_API_KEY

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def fetch_freshdesk_api(endpoint, params=None):
    """Generic Freshdesk API GET call."""
    headers = {"Content-Type": "application/json"}
    url = f"https://{FRESHDESK_DOMAIN}{endpoint}"
    if not FRESHDESK_API_KEY:
        logger.error("Freshdesk API Key not set.")
        return None
    try:
        response = requests.get(url, auth=(FRESHDESK_API_KEY, "X"), headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error hitting Freshdesk API {endpoint}: {e}")
        return None
