"""Tests for data collectors — mock HTTP responses, verify RawArticle output."""

import pytest
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock

from src.config import RawArticle


# --- RSS Collector ---

@pytest.mark.asyncio
async def test_rss_collector_parses_feed():
    """RSS collector should parse a feed and return RawArticle objects."""
    mock_feed_xml = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <title>Test Feed</title>
        <item>
          <title>Test AI Article</title>
          <link>https://example.com/article-1</link>
          <description>An article about AI advancements.</description>
          <pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>"""

    mock_response = MagicMock()
    mock_response.text = mock_feed_xml
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    with patch("src.collectors.rss_collector.RSS_FEEDS", [("test", "https://example.com/feed")]):
        from src.collectors.rss_collector import RSSCollector
        collector = RSSCollector()
        # Make cutoff very old so article passes filter
        collector.cutoff = datetime(2020, 1, 1, tzinfo=timezone.utc)

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            articles = await collector.collect()

        assert len(articles) >= 1
        assert all(isinstance(a, RawArticle) for a in articles)
        assert articles[0].source.startswith("rss:")


# --- HackerNews Collector ---

@pytest.mark.asyncio
async def test_hackernews_collector_filters_by_score():
    """HN collector should only return stories above the score threshold."""
    from src.collectors.hackernews import HackerNewsCollector

    top_stories = [1, 2, 3]
    items = {
        1: {"id": 1, "type": "story", "title": "AI breakthrough", "url": "https://example.com/ai", "score": 100},
        2: {"id": 2, "type": "story", "title": "Low score AI", "url": "https://example.com/low", "score": 10},
        3: {"id": 3, "type": "story", "title": "Another AI tool", "url": "https://example.com/tool", "score": 200},
    }

    async def mock_get(url, **kwargs):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.status_code = 200
        if "topstories" in url:
            resp.json = MagicMock(return_value=top_stories)
            resp.text = json.dumps(top_stories)
        elif "beststories" in url:
            resp.json = MagicMock(return_value=[])
            resp.text = "[]"
        elif "/item/" in url:
            item_id = int(url.split("/item/")[1].replace(".json", ""))
            resp.json = MagicMock(return_value=items.get(item_id, {}))
            resp.text = json.dumps(items.get(item_id, {}))
        else:
            resp.text = ""
        return resp

    mock_client = AsyncMock()
    mock_client.get = mock_get
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        collector = HackerNewsCollector()
        articles = await collector.collect()

    # Only items with score > 50 and AI keywords should be returned
    assert all(isinstance(a, RawArticle) for a in articles)
    assert all(a.score is None or a.score > 50 for a in articles if a.score)


# --- ArXiv Collector ---

@pytest.mark.asyncio
async def test_arxiv_collector_parses_response():
    """ArXiv collector should parse Atom XML and return RawArticle objects."""
    mock_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>A New Approach to Neural Networks</title>
        <summary>We present a novel architecture for deep learning.</summary>
        <id>http://arxiv.org/abs/2026.12345</id>
        <link href="http://arxiv.org/abs/2026.12345" rel="alternate" type="text/html"/>
        <link href="http://arxiv.org/pdf/2026.12345" type="application/pdf"/>
        <author><name>Jane Doe</name></author>
        <category term="cs.AI"/>
        <published>2026-01-15T00:00:00Z</published>
      </entry>
    </feed>"""

    mock_response = MagicMock()
    mock_response.text = mock_xml
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        from src.collectors.arxiv import ArxivCollector
        collector = ArxivCollector()
        collector.cutoff = datetime(2020, 1, 1, tzinfo=timezone.utc)
        articles = await collector.collect()

    assert len(articles) == 1
    assert articles[0].source == "arxiv"
    assert "Jane Doe" in articles[0].content
    assert isinstance(articles[0], RawArticle)


# --- Reddit Collector ---

@pytest.mark.asyncio
async def test_reddit_collector_parses_json():
    """Reddit collector should parse JSON API response."""
    mock_data = {
        "data": {
            "children": [
                {
                    "data": {
                        "title": "New ML framework released",
                        "url": "https://example.com/ml",
                        "selftext": "Check out this new framework.",
                        "score": 500,
                        "permalink": "/r/MachineLearning/comments/abc123/",
                    }
                }
            ]
        }
    }

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_data)
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    # Also mock the comments endpoint
    mock_comments = [
        {"data": {"children": []}},
        {"data": {"children": []}},
    ]
    mock_comments_response = MagicMock()
    mock_comments_response.json = MagicMock(return_value=mock_comments)
    mock_comments_response.status_code = 200
    mock_comments_response.raise_for_status = MagicMock()

    async def mock_get(url, **kwargs):
        if ".json?limit=5" in url:
            return mock_comments_response
        return mock_response

    mock_client = AsyncMock()
    mock_client.get = mock_get
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("src.collectors.reddit.SUBREDDITS", ["MachineLearning"]):
            from src.collectors.reddit import RedditCollector
            collector = RedditCollector()
            articles = await collector.collect()

    assert len(articles) >= 1
    assert articles[0].source == "reddit:r/MachineLearning"
    assert isinstance(articles[0], RawArticle)
