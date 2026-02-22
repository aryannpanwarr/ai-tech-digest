"""Reddit public JSON API collector."""

import asyncio

import httpx

from src.collectors.base import BaseCollector
from src.config import RawArticle, SUBREDDITS, HTTP_TIMEOUT, USER_AGENT


class RedditCollector(BaseCollector):
    def __init__(self):
        self.subreddits = SUBREDDITS
        self.min_score = 100

    async def collect(self) -> list[RawArticle]:
        articles = []
        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        ) as client:
            tasks = [self._fetch_subreddit(client, sub) for sub in self.subreddits]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    articles.extend(result)
                elif isinstance(result, Exception):
                    print(f"Reddit error: {result}")
        return articles

    async def _fetch_subreddit(
        self, client: httpx.AsyncClient, subreddit: str
    ) -> list[RawArticle]:
        articles = []
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit=10"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Failed to fetch r/{subreddit}: {e}")
            return []

        posts = data.get("data", {}).get("children", [])
        for post in posts:
            post_data = post.get("data", {})
            title = post_data.get("title", "")
            post_url = post_data.get("url", "")
            selftext = post_data.get("selftext", "")
            score = post_data.get("score", 0)
            permalink = post_data.get("permalink", "")

            if score < self.min_score:
                continue

            # Build content from selftext
            content = selftext if selftext else title

            # Fetch top comments for additional context
            if permalink:
                comments = await self._fetch_top_comments(client, permalink)
                if comments:
                    content += "\n\n--- Top Comments ---\n" + "\n".join(comments)

            articles.append(
                RawArticle(
                    title=title,
                    url=post_url or f"https://www.reddit.com{permalink}",
                    source=f"reddit:r/{subreddit}",
                    content=content,
                    score=score,
                    tags=[subreddit],
                )
            )

        print(f"  Reddit r/{subreddit}: {len(articles)} posts")
        return articles

    async def _fetch_top_comments(
        self, client: httpx.AsyncClient, permalink: str
    ) -> list[str]:
        try:
            url = f"https://www.reddit.com{permalink}.json?limit=5"
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

            comments = []
            if len(data) > 1:
                comment_listing = data[1].get("data", {}).get("children", [])
                for c in comment_listing[:5]:
                    body = c.get("data", {}).get("body", "")
                    if body and body != "[deleted]":
                        comments.append(body[:500])
            return comments
        except Exception:
            return []
