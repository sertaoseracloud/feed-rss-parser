from typing import List
from domain.post import Post
from ports.data_source import DataSourcePort
from ports.presenter import PresenterPort
from loguru import logger

class CollectPostsUseCase:
    def __init__(self, sources: List[DataSourcePort], presenter: PresenterPort):
        self.sources = sources
        self.presenter = presenter
        logger.trace("CollectPostsUseCase initialized with sources and presenter")

    def execute(self) -> None:
        logger.trace("Starting posts collection")
        all_posts: List[Post] = []
        for src in self.sources:
            posts = src.fetch_posts()
            if posts:
                logger.success(f"{src.__class__.__name__} → {len(posts)} post(s) obtained.")
            else:
                logger.warning(f"{src.__class__.__name__} → no posts obtained.")
            all_posts.extend(posts)
        logger.trace(f"Total posts collected: {len(all_posts)}")
        self.presenter.present(all_posts)
