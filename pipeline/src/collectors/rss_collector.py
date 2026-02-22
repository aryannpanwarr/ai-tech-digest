"""RSS feed collector using feedparser and httpx."""

import asyncio
from datetime import datetime, timedelta, timezone

import feedparser
import httpx

from src.collectors.base import BaseCollector
from src.config import RSS_FEEDS, RawArticle, HTTP_TIMEOUT, USER_AGENT


class RSSCollector(BaseCollector):
    def __init__(self):
        self.feeds = RSS_FEEDS
        self.cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    async def collect(self) -> list[RawArticle]:
        articles = []
        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        ) as client:
            tasks = [self._fetch_feed(client, name, url) for name, url in self.feeds]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    articles.extend(result)
                elif isinstance(result, Exception):
                    print(f"RSS feed error: {result}")
        return articles

    async def _fetch_feed(
        self, client: httpx.AsyncClient, source_name: str, feed_url: str
    ) -> list[RawArticle]:
        articles = []
        try:
            resp = await client.get(feed_url)
            resp.raise_for_status()
            feed = feedparser.parse(resp.text)
        except Exception as e:
            print(f"Failed to fetch RSS feed {source_name}: {e}")
            return []

        for entry in feed.entries:
            published = self._parse_date(entry)
            if published and published < self.cutoff:
                continue

            url = entry.get("link", "")
            if not url:
                continue

            # Try to fetch full article content
            content = await self._fetch_full_content(client, url)
            if not content:
                # Fallback to RSS summary
                content = entry.get("summary", "") or entry.get("description", "")

            title = entry.get("title", "Untitled")
            tags = [t.get("term", "") for t in entry.get("tags", [])]

            articles.append(
                RawArticle(
                    title=title,
                    url=url,
                    source=f"rss:{source_name}",
                    content=content,
                    published_at=published,
                    tags=tags,
                )
            )

        print(f"  RSS {source_name}: {len(articles)} articles")
        return articles

    async def _fetch_full_content(self, client: httpx.AsyncClient, url: str) -> str:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            # Return raw HTML text — the analyzer will handle extraction
            # For now, take a reasonable chunk of text content
            text = resp.text
            if len(text) > 50000:
                text = text[:50000]
            return text
        except Exception:
            return ""

    def _parse_date(self, entry) -> datetime | None:
        for field in ("published_parsed", "updated_parsed"):
            parsed = entry.get(field)
            if parsed:
                try:
                    from time import mktime
                    return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
                except Exception:
                    continue
        return None
