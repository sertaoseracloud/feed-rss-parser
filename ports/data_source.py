from abc import ABC, abstractmethod
from typing import List
from domain.post import Post

class DataSourcePort(ABC):
    @abstractmethod
    def fetch_posts(self) -> List[Post]:
        """Return a list of domain.Post objects"""
        pass