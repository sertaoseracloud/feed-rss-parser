from abc import ABC, abstractmethod
from typing import List
from domain.post import Post

class PresenterPort(ABC):
    @abstractmethod
    def present(self, posts: List[Post]) -> None:
        """Handle the output of collected posts"""
        pass