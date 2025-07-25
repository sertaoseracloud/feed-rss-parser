import os
from datetime import datetime
from typing import List
from domain.post import Post
from ports.presenter import PresenterPort
from loguru import logger

class MarkdownPresenter(PresenterPort):
    def __init__(self, output_dir: str = "pautas_md"):
        self.base_output_dir = output_dir
        # Create a subfolder for the current date
        self.date_folder = datetime.now().strftime("%Y-%m-%d")
        self.output_dir = os.path.join(self.base_output_dir, self.date_folder)
        os.makedirs(self.output_dir, exist_ok=True)
        logger.trace(f"MarkdownPresenter initialized at {self.output_dir}")

    def present(self, posts: List[Post]) -> None:
        logger.trace(f"Saving {len(posts)} posts to markdown in {self.output_dir}")
        categories = {}
        for post in posts:
            categories.setdefault(post.categoria, []).append(post)

        for cat, items in categories.items():
            path = f"{self.output_dir}/{cat.replace(' ', '_').lower()}.md"
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"# Pautas: {cat}\n\n")
                    for item in items:
                        f.write(f"## {item.titulo}\n")
                        f.write(f"{item.resumo}\n\n")
                        f.write(f"🔗 [Acessar fonte]({item.link})\n\n")
                        f.write(" ".join(item.hashtags) + "\n\n---\n\n")
                logger.success(f"Saved {len(items)} posts to {path}")
            except Exception as e:
                logger.error(f"Failed to save {cat}: {e}")
