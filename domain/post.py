from dataclasses import dataclass
from typing import List

@dataclass
class Post:
    origem: str
    categoria: str
    titulo: str
    resumo: str
    link: str
    engajamento: int
    hashtags: List[str]