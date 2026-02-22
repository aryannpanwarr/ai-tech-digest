"""Tests for publisher — verify markdown output matches the data contract."""

import json
import os
import tempfile
import pytest
import yaml

from src.publisher.markdown_writer import write_post, update_resources


@pytest.fixture
def temp_content_dir(tmp_path, monkeypatch):
    """Set up a temporary content directory for testing."""
    posts_dir = tmp_path / "content" / "posts"
    posts_dir.mkdir(parents=True)
    resources_path = tmp_path / "content" / "resources.json"

    # Write initial resources.json
    initial_resources = {
        "last_updated": "2026-01-01",
        "categories": {
            "newsletters": [],
            "podcasts": [],
            "youtube_channels": [],
            "blogs": [],
            "research_trackers": [],
            "tools": [],
            "communities": [],
        },
    }
    resources_path.write_text(json.dumps(initial_resources))

    # Monkeypatch the paths
    monkeypatch.setattr(
        "src.publisher.markdown_writer.POSTS_DIR",
        str(posts_dir),
    )
    monkeypatch.setattr(
        "src.publisher.markdown_writer.RESOURCES_PATH",
        str(resources_path),
    )

    return tmp_path


class TestMarkdownWriter:
    def test_write_post_creates_valid_markdown(self, temp_content_dir):
        triage = {
            "stories": [
                {
                    "headline": "Test Story One",
                    "category": "ai-research",
                    "significance": 9,
                    "source_article_indices": [0],
                    "one_line_summary": "A major AI breakthrough.",
                    "source_url": "https://example.com/story1",
                },
                {
                    "headline": "Test Story Two",
                    "category": "tech",
                    "significance": 7,
                    "source_article_indices": [1],
                    "one_line_summary": "New tech development.",
                    "source_url": "https://example.com/story2",
                },
            ]
        }

        analysis = "## This Week in AI & Tech\n\n> Big things happened.\n\n## The Big Story\n\nDetails here."

        resources = {
            "resources": [
                {
                    "title": "Test Paper",
                    "url": "https://example.com/paper",
                    "type": "paper",
                    "description": "A great paper.",
                }
            ]
        }

        post_path = write_post(triage, analysis, resources)
        assert os.path.exists(post_path)
        assert post_path.endswith(".md")

        # Parse the file
        with open(post_path, "r") as f:
            content = f.read()

        # Split frontmatter and body
        parts = content.split("---")
        assert len(parts) >= 3, "File should have YAML frontmatter delimiters"

        frontmatter = yaml.safe_load(parts[1])

        # Verify frontmatter fields
        assert "title" in frontmatter
        assert "date" in frontmatter
        assert "week_number" in frontmatter
        assert "year" in frontmatter
        assert "summary" in frontmatter
        assert "top_stories" in frontmatter
        assert "categories" in frontmatter
        assert "resources" in frontmatter

        # Verify top_stories structure
        for story in frontmatter["top_stories"]:
            assert "title" in story
            assert "category" in story
            assert story["category"] in ["ai-research", "ai-industry", "tech", "open-source", "policy"]
            assert "significance" in story
            assert 1 <= story["significance"] <= 10
            assert "source_url" in story

        # Verify resources structure
        for resource in frontmatter["resources"]:
            assert "title" in resource
            assert "url" in resource
            assert "type" in resource
            assert resource["type"] in ["paper", "article", "tool", "repo", "video", "podcast", "newsletter"]
            assert "description" in resource

        # Verify body contains analysis
        body = "---".join(parts[2:])
        assert "## This Week" in body

    def test_write_post_validates_categories(self, temp_content_dir):
        """Invalid categories should be corrected to 'tech'."""
        triage = {
            "stories": [
                {
                    "headline": "Story",
                    "category": "invalid-category",
                    "significance": 5,
                    "source_article_indices": [],
                    "one_line_summary": "Test.",
                }
            ]
        }
        analysis = "Content"
        resources = {"resources": []}

        post_path = write_post(triage, analysis, resources)
        with open(post_path, "r") as f:
            content = f.read()

        parts = content.split("---")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["top_stories"][0]["category"] == "tech"

    def test_write_post_clamps_significance(self, temp_content_dir):
        """Significance should be clamped to 1-10."""
        triage = {
            "stories": [
                {
                    "headline": "Story",
                    "category": "tech",
                    "significance": 15,
                    "source_article_indices": [],
                    "one_line_summary": "Test.",
                }
            ]
        }
        analysis = "Content"
        resources = {"resources": []}

        post_path = write_post(triage, analysis, resources)
        with open(post_path, "r") as f:
            content = f.read()

        parts = content.split("---")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["top_stories"][0]["significance"] == 10


class TestUpdateResources:
    def test_merges_new_resources(self, temp_content_dir):
        resources = {
            "resources": [
                {
                    "title": "New Tool",
                    "url": "https://example.com/tool",
                    "type": "tool",
                    "description": "A useful tool.",
                },
                {
                    "title": "New Paper",
                    "url": "https://example.com/paper",
                    "type": "paper",
                    "description": "A great paper.",
                },
            ]
        }

        update_resources(resources)

        resources_path = os.path.join(str(temp_content_dir), "content", "resources.json")
        with open(resources_path, "r") as f:
            data = json.load(f)

        assert data["last_updated"]
        # tool should go to tools category
        assert any(r["name"] == "New Tool" for r in data["categories"]["tools"])
        # paper should go to research_trackers
        assert any(r["name"] == "New Paper" for r in data["categories"]["research_trackers"])

    def test_does_not_duplicate_existing_urls(self, temp_content_dir):
        resources_path = os.path.join(str(temp_content_dir), "content", "resources.json")

        # Pre-populate with a resource
        initial = {
            "last_updated": "2026-01-01",
            "categories": {
                "tools": [{"name": "Existing", "url": "https://example.com/tool", "description": "Exists"}],
                "newsletters": [], "podcasts": [], "youtube_channels": [],
                "blogs": [], "research_trackers": [], "communities": [],
            },
        }
        with open(resources_path, "w") as f:
            json.dump(initial, f)

        resources = {
            "resources": [
                {"title": "Existing", "url": "https://example.com/tool", "type": "tool", "description": "Same URL"},
            ]
        }

        update_resources(resources)

        with open(resources_path, "r") as f:
            data = json.load(f)

        tools = data["categories"]["tools"]
        urls = [t["url"] for t in tools]
        assert urls.count("https://example.com/tool") == 1
