"""Generates markdown post matching the shared data contract and updates resources.json."""

import json
import os
from datetime import datetime, timedelta, timezone

import yaml

from src.config import RawArticle, VALID_CATEGORIES, VALID_RESOURCE_TYPES

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "content")
POSTS_DIR = os.path.join(CONTENT_DIR, "posts")
RESOURCES_PATH = os.path.join(CONTENT_DIR, "resources.json")


def _get_current_sunday() -> datetime:
    """Get the most recent Sunday date (or today if it's Sunday)."""
    now = datetime.now(timezone.utc)
    days_since_sunday = (now.weekday() - 6) % 7
    sunday = now - timedelta(days=days_since_sunday)
    return sunday.replace(hour=0, minute=0, second=0, microsecond=0)


def _extract_source_indices(story: dict) -> list[int]:
    """Handle both modern and legacy source-index keys from LLM output."""
    indices = story.get("source_article_indices")
    if isinstance(indices, list):
        return [idx for idx in indices if isinstance(idx, int)]

    legacy = story.get("source_articles")
    if isinstance(legacy, list):
        return [idx for idx in legacy if isinstance(idx, int)]

    return []


def write_post(
    triage: dict,
    analysis: str,
    resources: dict,
    source_articles: list[RawArticle] | None = None,
) -> str:
    """Write the weekly digest markdown post matching the data contract.

    Args:
        triage: Dict with 'stories' list from triage step.
        analysis: Full markdown analysis text from deep analysis step.
        resources: Dict with 'resources' list from resource curation step.

    Returns:
        Path to the written post file.
    """
    os.makedirs(POSTS_DIR, exist_ok=True)

    sunday = _get_current_sunday()
    date_str = sunday.strftime("%Y-%m-%d")
    week_number = sunday.isocalendar()[1]
    year = sunday.year

    # Build top_stories from triage
    top_stories = []
    for story in triage.get("stories", []):
        category = story.get("category", "tech")
        if category not in VALID_CATEGORIES:
            category = "tech"

        significance = story.get("significance", 5)
        significance = max(1, min(10, significance))

        # Prefer the URL selected during triage, otherwise map source indices to articles.
        source_url = story.get("source_url", "")
        if not source_url and source_articles:
            indices = _extract_source_indices(story)
            for idx in indices:
                if 0 <= idx < len(source_articles):
                    candidate = source_articles[idx].url.strip()
                    if candidate:
                        source_url = candidate
                        break

        top_stories.append({
            "title": story.get("headline", "Untitled"),
            "category": category,
            "significance": significance,
            "source_url": source_url,
        })

    # Build categories list from stories
    categories = list(set(s["category"] for s in top_stories))
    categories.sort()

    # Build resources list
    post_resources = []
    for resource in resources.get("resources", []):
        res_type = resource.get("type", "article")
        if res_type not in VALID_RESOURCE_TYPES:
            res_type = "article"

        post_resources.append({
            "title": resource.get("title", ""),
            "url": resource.get("url", ""),
            "type": res_type,
            "description": resource.get("description", ""),
        })

    # Build summary from the first story or analysis
    stories = triage.get("stories", [])
    if stories:
        summaries = [s.get("one_line_summary", s.get("headline", "")) for s in stories[:3]]
        summary = " ".join(summaries)
    else:
        summary = "This week's AI and tech digest."

    # Build frontmatter
    frontmatter = {
        "title": f"AI & Tech Weekly Digest — Week of {sunday.strftime('%B %d, %Y')}",
        "date": date_str,
        "week_number": week_number,
        "year": year,
        "summary": summary,
        "top_stories": top_stories,
        "categories": categories,
        "resources": post_resources,
    }

    # Serialize frontmatter to YAML
    frontmatter_yaml = yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )

    # Assemble the full markdown file
    post_content = f"---\n{frontmatter_yaml}---\n\n{analysis}\n"

    # Write to file
    post_path = os.path.join(POSTS_DIR, f"{date_str}.md")
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post_content)

    print(f"  Written post: {post_path}")
    return post_path


def update_resources(resources: dict) -> None:
    """Merge new resources into existing resources.json without overwriting.

    Adds new resources to the appropriate category lists based on resource type.
    """
    # Load existing resources
    existing = {"last_updated": "", "categories": {
        "newsletters": [],
        "podcasts": [],
        "youtube_channels": [],
        "blogs": [],
        "research_trackers": [],
        "tools": [],
        "communities": [],
    }}

    if os.path.exists(RESOURCES_PATH):
        try:
            with open(RESOURCES_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  Warning: Could not read resources.json: {e}")

    # Map resource types to category keys
    type_to_category = {
        "newsletter": "newsletters",
        "podcast": "podcasts",
        "video": "youtube_channels",
        "article": "blogs",
        "paper": "research_trackers",
        "tool": "tools",
        "repo": "tools",
    }

    # Collect existing URLs to avoid duplicates
    existing_urls = set()
    for category_items in existing.get("categories", {}).values():
        for item in category_items:
            existing_urls.add(item.get("url", ""))

    # Add new resources
    new_count = 0
    for resource in resources.get("resources", []):
        url = resource.get("url", "")
        if url in existing_urls:
            continue

        res_type = resource.get("type", "article")
        category_key = type_to_category.get(res_type, "blogs")

        if category_key not in existing["categories"]:
            existing["categories"][category_key] = []

        existing["categories"][category_key].append({
            "name": resource.get("title", ""),
            "url": url,
            "description": resource.get("description", ""),
        })
        existing_urls.add(url)
        new_count += 1

    # Update timestamp
    existing["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Write back
    os.makedirs(os.path.dirname(RESOURCES_PATH), exist_ok=True)
    with open(RESOURCES_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"  Updated resources.json: {new_count} new resources added")
