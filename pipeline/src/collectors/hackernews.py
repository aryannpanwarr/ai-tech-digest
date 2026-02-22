"""HackerNews API collector."""

import asyncio

import httpx

from src.collectors.base import BaseCollector
from src.config import RawArticle, AI_TECH_KEYWORDS, HTTP_TIMEOUT, USER_AGENT

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


class HackerNewsCollector(BaseCollector):
    def __init__(self):
        self.min_score = 50
        self.max_stories = 30

    async def collect(self) -> list[RawArticle]:
        articles = []
        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        ) as client:
            # Fetch both top and best story IDs
            story_ids = set()
            for endpoint in ("topstories", "beststories"):
                try:
                    resp = await client.get(f"{HN_API_BASE}/{endpoint}.json")
                    resp.raise_for_status()
                    ids = resp.json()
                    story_ids.update(ids[:50])  # Take top 50 from each
                except Exception as e:
                    print(f"HN {endpoint} fetch error: {e}")

            # Fetch individual stories concurrently
            sem = asyncio.Semaphore(10)  # Limit concurrent requests
            tasks = [self._fetch_story(client, sem, sid) for sid in story_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, RawArticle):
                    articles.append(result)

        # Sort by score and limit
        articles.sort(key=lambda a: a.score or 0, reverse=True)
        articles = articles[: self.max_stories]
        print(f"  HackerNews: {len(articles)} articles")
        return articles

    async def _fetch_story(
        self, client: httpx.AsyncClient, sem: asyncio.Semaphore, story_id: int
    ) -> RawArticle | None:
        async with sem:
            try:
                resp = await client.get(f"{HN_API_BASE}/item/{story_id}.json")
                resp.raise_for_status()
                item = resp.json()
            except Exception:
                return None

            if not item or item.get("type") != "story":
                return None

            score = item.get("score", 0)
            if score < self.min_score:
                return None

            title = item.get("title", "")
            url = item.get("url", f"https://news.ycombinator.com/item?id={story_id}")

            # Filter for AI/tech relevance
            if not self._is_relevant(title, url):
                return None

            # Try to fetch linked article content
            content = ""
            if url and not url.startswith("https://news.ycombinator.com"):
                content = await self._fetch_content(client, url)

            # Include HN text (for Ask HN, Show HN posts)
            hn_text = item.get("text", "")
            if hn_text:
                content = f"{hn_text}\n\n{content}" if content else hn_text

            if not content:
                content = title

            return RawArticle(
                title=title,
                url=url,
                source="hackernews",
                content=content,
                score=score,
                tags=["hackernews"],
            )

    async def _fetch_content(self, client: httpx.AsyncClient, url: str) -> str:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            text = resp.text
            if len(text) > 50000:
                text = text[:50000]
            return text
        except Exception:
            return ""

    def _is_relevant(self, title: str, url: str) -> bool:
        text = f"{title} {url}".lower()
        return any(kw in text for kw in AI_TECH_KEYWORDS)
