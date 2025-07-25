import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from domain.post import Post
from ports.data_source import DataSourcePort
from utils.tags import gerar_hashtags_por_categoria
from loguru import logger

class RedditAdapter(DataSourcePort):
    def __init__(self, subreddit: str, category: str, limit: int = 5, verify_ssl: bool = False):
        self.subreddit = subreddit
        self.category = category
        self.limit = limit
        self.url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        self.headers = {"User-Agent": "trend-analyzer"}
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.session = self._create_session()
        logger.trace(f"Initialized RedditAdapter for /r/{self.subreddit} (verify_ssl={self.verify_ssl})")

    def _create_session(self):
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def fetch_posts(self):
        logger.trace(f"Fetching Reddit posts from /r/{self.subreddit} (limit={self.limit})")
        posts = []
        try:
            resp = self.session.get(self.url, headers=self.headers, timeout=10, verify=self.verify_ssl)
            logger.debug(f"Reddit response status for /r/{self.subreddit}: {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            total_items = len(data.get("data", {}).get("children", []))
            logger.debug(f"/r/{self.subreddit} returned {total_items} items before filtering")
        except requests.exceptions.SSLError:
            logger.error(f"SSL error fetching {self.url}. Try setting verify_ssl=False if needed.")
            return posts
        except Exception as e:
            logger.error(f"Error fetching {self.url}: {e}")
            return posts

        for child in data.get("data", {}).get("children", []):
            p = child.get("data", {})
            if p.get("stickied"):
                logger.trace(f"Skipping stickied post: {p.get('title')}")
                continue
            posts.append(
                Post(
                    origem="reddit",
                    categoria=self.category,
                    titulo=p.get("title", "Sem título"),
                    resumo=p.get("selftext", "")[:300].strip(),
                    link="https://reddit.com" + p.get("permalink", ""),
                    engajamento=p.get("ups", 0) + p.get("num_comments", 0),
                    hashtags=gerar_hashtags_por_categoria(self.category),
                )
            )
        logger.success(f"Fetched {len(posts)} posts from /r/{self.subreddit} (non-stickied)")
        return posts
