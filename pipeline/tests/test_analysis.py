"""Tests for analysis pipeline — mock Gemini API, verify JSON parsing."""

import json
import pytest
from unittest.mock import patch, MagicMock

from src.config import RawArticle


def _make_articles(n: int = 5) -> list[RawArticle]:
    """Create sample RawArticle objects for testing."""
    return [
        RawArticle(
            title=f"Test Article {i}",
            url=f"https://example.com/article-{i}",
            source="test",
            content=f"Content for article {i} about AI developments.",
            score=100 - i * 10,
            tags=["ai", "test"],
        )
        for i in range(n)
    ]


# --- Deduplicator Tests ---

class TestDeduplicator:
    def test_url_normalization(self):
        from src.analysis.deduplicator import normalize_url

        assert normalize_url("https://www.example.com/page/") == normalize_url("https://example.com/page")
        assert normalize_url("https://example.com/page?utm_source=twitter") == normalize_url("https://example.com/page")

    def test_deduplicates_same_url(self):
        from src.analysis.deduplicator import deduplicate

        articles = [
            RawArticle(title="Article A", url="https://example.com/page", source="rss", content="Short"),
            RawArticle(title="Article A copy", url="https://www.example.com/page/", source="hn", content="Much longer content here with more detail"),
        ]
        result = deduplicate(articles)
        assert len(result) == 1
        # Should keep the longer content
        assert "Much longer" in result[0].content

    def test_deduplicates_fuzzy_titles(self):
        from src.analysis.deduplicator import deduplicate

        articles = [
            RawArticle(title="Google Releases Gemini 2.5", url="https://a.com/1", source="rss", content="Content A"),
            RawArticle(title="Google Releases Gemini 2.5 Ultra", url="https://b.com/2", source="hn", content="Content B is longer than A"),
        ]
        result = deduplicate(articles)
        assert len(result) == 1

    def test_keeps_different_articles(self):
        from src.analysis.deduplicator import deduplicate

        articles = [
            RawArticle(title="AI breakthrough in protein folding", url="https://a.com/1", source="rss", content="A"),
            RawArticle(title="New JavaScript framework released", url="https://b.com/2", source="hn", content="B"),
        ]
        result = deduplicate(articles)
        assert len(result) == 2

    def test_merges_tags(self):
        from src.analysis.deduplicator import deduplicate

        articles = [
            RawArticle(title="Same Article", url="https://example.com/page", source="rss", content="Content", tags=["ai"]),
            RawArticle(title="Same Article", url="https://example.com/page", source="hn", content="Content longer version", tags=["ml", "research"]),
        ]
        result = deduplicate(articles)
        assert len(result) == 1
        assert set(result[0].tags) == {"ai", "ml", "research"}

    def test_empty_input(self):
        from src.analysis.deduplicator import deduplicate
        assert deduplicate([]) == []


# --- Analyzer Tests (mocked Gemini API) ---

class TestAnalyzer:
    @pytest.mark.asyncio
    async def test_triage_parses_valid_json(self):
        mock_triage_response = {
            "stories": [
                {
                    "headline": "Test Story",
                    "category": "ai-research",
                    "significance": 8,
                    "source_article_indices": [0, 1],
                    "one_line_summary": "Something happened."
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_triage_response)
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=100, candidates_token_count=50
        )

        mock_client = MagicMock()
        mock_client.models.generate_content = MagicMock(return_value=mock_response)

        with patch("src.analysis.analyzer._get_client", return_value=mock_client):
            from src.analysis.analyzer import triage_articles
            result = await triage_articles(_make_articles())

        assert "stories" in result
        assert len(result["stories"]) == 1
        assert result["stories"][0]["category"] == "ai-research"

    @pytest.mark.asyncio
    async def test_triage_handles_markdown_fenced_json(self):
        mock_json = {"stories": [{"headline": "Test", "category": "tech", "significance": 5, "source_article_indices": [], "one_line_summary": "Test."}]}
        response_text = f"```json\n{json.dumps(mock_json)}\n```"

        mock_response = MagicMock()
        mock_response.text = response_text
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=100, candidates_token_count=50
        )

        mock_client = MagicMock()
        mock_client.models.generate_content = MagicMock(return_value=mock_response)

        with patch("src.analysis.analyzer._get_client", return_value=mock_client):
            from src.analysis.analyzer import triage_articles
            result = await triage_articles(_make_articles())

        assert "stories" in result

    @pytest.mark.asyncio
    async def test_deep_analysis_returns_markdown(self):
        mock_response = MagicMock()
        mock_response.text = "## This Week in AI & Tech\n\n> Summary here.\n\n## The Big Story\n\nDetails."
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=500, candidates_token_count=200
        )

        mock_client = MagicMock()
        mock_client.models.generate_content = MagicMock(return_value=mock_response)

        triage = {"stories": [{"headline": "Test", "source_article_indices": [0]}]}

        with patch("src.analysis.analyzer._get_client", return_value=mock_client):
            from src.analysis.analyzer import deep_analysis
            result = await deep_analysis(triage, _make_articles())

        assert "## This Week" in result
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_curate_resources_parses_json(self):
        mock_resources = {
            "resources": [
                {
                    "title": "Test Resource",
                    "url": "https://example.com/resource",
                    "type": "paper",
                    "description": "A useful resource."
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_resources)
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=100, candidates_token_count=50
        )

        mock_client = MagicMock()
        mock_client.models.generate_content = MagicMock(return_value=mock_response)

        triage = {"stories": []}

        with patch("src.analysis.analyzer._get_client", return_value=mock_client):
            from src.analysis.analyzer import curate_resources
            result = await curate_resources(triage, _make_articles())

        assert "resources" in result
        assert len(result["resources"]) == 1
