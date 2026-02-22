"""GitHub trending repositories collector using the Search API."""

import os
from datetime import datetime, timedelta, timezone

import httpx

from src.collectors.base import BaseCollector
from src.config import RawArticle, HTTP_TIMEOUT, USER_AGENT

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

# AI/ML topic keywords to search for
GITHUB_TOPICS = [
    "machine-learning",
    "deep-learning",
    "artificial-intelligence",
    "llm",
    "large-language-model",
    "generative-ai",
    "nlp",
    "computer-vision",
    "transformers",
]


class GitHubTrendingCollector(BaseCollector):
    async def collect(self) -> list[RawArticle]:
        articles = []
        date_cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

        headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github.v3+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"

        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            headers=headers,
            follow_redirects=True,
        ) as client:
            for topic in GITHUB_TOPICS:
                try:
                    repos = await self._search_topic(client, topic, date_cutoff)
                    articles.extend(repos)
                except Exception as e:
                    print(f"GitHub search error for {topic}: {e}")

        # Deduplicate by repo URL and sort by stars
        seen_urls = set()
        unique = []
        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique.append(article)

        unique.sort(key=lambda a: a.score or 0, reverse=True)
        unique = unique[:30]
        print(f"  GitHub Trending: {len(unique)} repos")
        return unique

    async def _search_topic(
        self, client: httpx.AsyncClient, topic: str, date_cutoff: str
    ) -> list[RawArticle]:
        query = f"topic:{topic} stars:>50 pushed:>{date_cutoff}"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": "10",
        }

        try:
            resp = await client.get(GITHUB_SEARCH_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"GitHub API error: {e}")
            return []

        articles = []
        for repo in data.get("items", []):
            name = repo.get("full_name", "")
            description = repo.get("description", "") or ""
            stars = repo.get("stargazers_count", 0)
            language = repo.get("language", "")
            url = repo.get("html_url", "")
            topics = repo.get("topics", [])

            # Build content
            content_parts = [description]
            if language:
                content_parts.append(f"Language: {language}")
            content_parts.append(f"Stars: {stars}")
            if topics:
                content_parts.append(f"Topics: {', '.join(topics)}")

            # Try to fetch README excerpt
            readme = await self._fetch_readme(client, name)
            if readme:
                content_parts.append(f"\nREADME excerpt:\n{readme[:2000]}")

            articles.append(
                RawArticle(
                    title=name,
                    url=url,
                    source="github",
                    content="\n".join(content_parts),
                    score=stars,
                    tags=topics or [topic],
                )
            )

        return articles

    async def _fetch_readme(self, client: httpx.AsyncClient, repo_name: str) -> str:
        try:
            resp = await client.get(
                f"https://api.github.com/repos/{repo_name}/readme",
                headers={"Accept": "application/vnd.github.raw"},
            )
            if resp.status_code == 200:
                return resp.text[:2000]
        except Exception:
            pass
        return ""
