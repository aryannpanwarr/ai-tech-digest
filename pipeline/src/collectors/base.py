"""Abstract base collector class."""

from abc import ABC, abstractmethod
from src.config import RawArticle


class BaseCollector(ABC):
    @abstractmethod
    async def collect(self) -> list[RawArticle]:
        pass
