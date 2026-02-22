"""ArXiv API collector for AI/ML papers."""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import httpx

from src.collectors.base import BaseCollector
from src.config import RawArticle, ARXIV_CATEGORIES, ARXIV_MAX_RESULTS, HTTP_TIMEOUT, USER_AGENT

ARXIV_API_URL = "http://export.arxiv.org/api/query"
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


class ArxivCollector(BaseCollector):
    def __init__(self):
        self.cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    async def collect(self) -> list[RawArticle]:
        articles = []
        query = " OR ".join(f"cat:{cat}" for cat in ARXIV_CATEGORIES)
        params = {
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": str(ARXIV_MAX_RESULTS),
        }

        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            try:
                resp = await client.get(ARXIV_API_URL, params=params)
                resp.raise_for_status()
            except Exception as e:
                print(f"ArXiv API error: {e}")
                return []

        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError as e:
            print(f"ArXiv XML parse error: {e}")
            return []

        for entry in root.findall("atom:entry", ARXIV_NS):
            title_el = entry.find("atom:title", ARXIV_NS)
            title = title_el.text.strip().replace("\n", " ") if title_el is not None else "Untitled"

            summary_el = entry.find("atom:summary", ARXIV_NS)
            abstract = summary_el.text.strip() if summary_el is not None else ""

            # Get the arxiv URL
            url = ""
            pdf_url = ""
            for link in entry.findall("atom:link", ARXIV_NS):
                href = link.get("href", "")
                link_type = link.get("type", "")
                rel = link.get("rel", "")
                if link_type == "text/html" or rel == "alternate":
                    url = href
                elif "pdf" in href or link_type == "application/pdf":
                    pdf_url = href

            if not url:
                id_el = entry.find("atom:id", ARXIV_NS)
                url = id_el.text.strip() if id_el is not None else ""

            # Get authors
            authors = []
            for author in entry.findall("atom:author", ARXIV_NS):
                name_el = author.find("atom:name", ARXIV_NS)
                if name_el is not None:
                    authors.append(name_el.text.strip())

            # Get categories
            tags = []
            for cat in entry.findall("atom:category", ARXIV_NS):
                term = cat.get("term", "")
                if term:
                    tags.append(term)

            # Published date
            published_el = entry.find("atom:published", ARXIV_NS)
            published_at = None
            if published_el is not None:
                try:
                    date_str = published_el.text.strip()
                    published_at = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except Exception:
                    pass

            # Keep the feed focused on the last 7 days.
            if published_at and published_at < self.cutoff:
                continue

            content = f"Authors: {', '.join(authors)}\n\n{abstract}"
            if pdf_url:
                content += f"\n\nPDF: {pdf_url}"

            articles.append(
                RawArticle(
                    title=title,
                    url=url,
                    source="arxiv",
                    content=content,
                    published_at=published_at,
                    tags=tags,
                )
            )

        print(f"  ArXiv: {len(articles)} papers")
        return articles
