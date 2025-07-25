import feedparser
from bs4 import BeautifulSoup
from domain.post import Post
from ports.data_source import DataSourcePort
from utils.tags import gerar_hashtags_por_categoria
from loguru import logger
import requests
import urllib3

class RSSAdapter(DataSourcePort):
    def __init__(self, name: str, category: str, feed_url: str, top_n: int = 5, verify_ssl: bool = False):
        self.name = name
        self.category = category
        self.feed_url = feed_url  
        self.top_n = top_n
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.trace(f"Initialized RSSAdapter for {self.name} ({self.feed_url}) (verify_ssl={self.verify_ssl})")

    def _validate_url(self, url):
        try:
            response = requests.get(url, allow_redirects=True, timeout=10, verify=self.verify_ssl)
            final_url = response.url
            logger.debug(f"Validated URL {url} → {final_url} - Status: {response.status_code}")
            if response.status_code >= 400:
                logger.warning(f"Feed URL not reachable or returned error ({response.status_code}): {final_url}")
                return False
            return True
        except requests.exceptions.SSLError:
            logger.error(f"SSL error validating URL {url}. Try setting verify_ssl=False if needed.")
            return False
        except requests.exceptions.ConnectionError as ce:
            logger.error(f"Connection error validating URL {url}: {ce}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating URL {url}: {e}")
            return False

    def fetch_posts(self):
        logger.trace(f"Fetching RSS feed for {self.name}")
        posts = []
        if not self._validate_url(self.feed_url):
            return posts
        try:
            feed = feedparser.parse(self.feed_url)
            logger.debug(f"Feed status: {getattr(feed, 'status', 'unknown')} - entries: {len(feed.entries)}")
            if not feed.entries:
                logger.warning(f"No entries returned for {self.feed_url}")
                return posts
        except Exception as e:
            logger.error(f"Error fetching feed {self.feed_url}: {e}")
            return posts

        for entry in feed.entries[:self.top_n]:
            raw = entry.get("summary", "") or entry.get("content", [{}])[0].get("value", "")
            resumo = BeautifulSoup(raw, "html.parser").get_text()[:300].strip()
            posts.append(
                Post(
                    origem="rss",
                    categoria=self.category,
                    titulo=entry.get("title", "Sem título"),
                    resumo=resumo,
                    link=entry.get("link", ""),
                    engajamento=0,
                    hashtags=gerar_hashtags_por_categoria(self.category),
                )
            )
        logger.success(f"Fetched {len(posts)} posts from {self.name}")
        return posts
