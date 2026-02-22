"""Gemini API-based analysis pipeline using google-genai SDK."""

import json
import os

from google import genai

from src.analysis.prompts import TRIAGE_PROMPT, ANALYSIS_PROMPT, RESOURCES_PROMPT
from src.config import RawArticle

# Model configuration
FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash-preview-05-20")
PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3-pro")


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")
    return genai.Client(api_key=api_key)


def _parse_json_response(text: str) -> dict:
    """Parse JSON from LLM response, handling potential markdown fencing."""
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first line (```json or ```) and last line (```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    return json.loads(text)


def _articles_to_json(articles: list[RawArticle], max_content_len: int = 2000) -> str:
    """Convert articles to a JSON string for LLM input, truncating content."""
    items = []
    for i, article in enumerate(articles):
        content = article.content[:max_content_len]
        items.append({
            "index": i,
            "title": article.title,
            "url": article.url,
            "source": article.source,
            "content": content,
            "score": article.score,
            "tags": article.tags,
        })
    return json.dumps(items, indent=2)


async def triage_articles(articles: list[RawArticle]) -> dict:
    """Call 1 — Triage and categorize articles using Gemini Flash.

    Returns dict with 'stories' key containing list of triaged stories.
    """
    client = _get_client()
    articles_json = _articles_to_json(articles)

    user_message = f"Here are the collected articles from this week:\n\n{articles_json}"

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=FLASH_MODEL,
                contents=[
                    {"role": "user", "parts": [{"text": f"{TRIAGE_PROMPT}\n\n{user_message}"}]}
                ],
                config={
                    "temperature": 0.3,
                    "max_output_tokens": 2000,
                },
            )

            result = _parse_json_response(response.text)

            # Log token usage
            if hasattr(response, "usage_metadata"):
                usage = response.usage_metadata
                print(f"  Triage tokens — input: {usage.prompt_token_count}, output: {usage.candidates_token_count}")

            return result
        except json.JSONDecodeError:
            if attempt == 0:
                print("  Triage JSON parse failed, retrying...")
                continue
            raise
        except Exception as e:
            if attempt == 0:
                print(f"  Triage error, retrying: {e}")
                continue
            raise

    return {"stories": []}


async def deep_analysis(triage: dict, articles: list[RawArticle]) -> str:
    """Call 2 — Deep analysis using Gemini Pro.

    Returns the full markdown analysis text.
    """
    client = _get_client()

    # Build context: triaged stories + relevant source material
    stories_context = json.dumps(triage.get("stories", []), indent=2)

    # Gather source articles referenced by the triage
    referenced_indices = set()
    for story in triage.get("stories", []):
        for idx in story.get("source_article_indices", []):
            referenced_indices.add(idx)

    source_material = []
    for idx in sorted(referenced_indices):
        if idx < len(articles):
            a = articles[idx]
            source_material.append({
                "index": idx,
                "title": a.title,
                "url": a.url,
                "source": a.source,
                "content": a.content[:3000],
            })

    source_json = json.dumps(source_material, indent=2)
    user_message = f"Triaged stories:\n{stories_context}\n\nSource material:\n{source_json}"

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=PRO_MODEL,
                contents=[
                    {"role": "user", "parts": [{"text": f"{ANALYSIS_PROMPT}\n\n{user_message}"}]}
                ],
                config={
                    "temperature": 0.7,
                    "max_output_tokens": 8000,
                },
            )

            if hasattr(response, "usage_metadata"):
                usage = response.usage_metadata
                print(f"  Analysis tokens — input: {usage.prompt_token_count}, output: {usage.candidates_token_count}")

            return response.text
        except Exception as e:
            if attempt == 0:
                print(f"  Analysis error, retrying: {e}")
                continue
            raise

    return ""


async def curate_resources(triage: dict, articles: list[RawArticle]) -> dict:
    """Call 3 — Resource curation using Gemini Flash.

    Returns dict with 'resources' key containing list of curated resources.
    """
    client = _get_client()

    stories_context = json.dumps(triage.get("stories", []), indent=2)
    articles_summary = _articles_to_json(articles[:50], max_content_len=500)

    user_message = (
        f"Top stories this week:\n{stories_context}\n\n"
        f"All collected articles:\n{articles_summary}"
    )

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=FLASH_MODEL,
                contents=[
                    {"role": "user", "parts": [{"text": f"{RESOURCES_PROMPT}\n\n{user_message}"}]}
                ],
                config={
                    "temperature": 0.3,
                    "max_output_tokens": 2000,
                },
            )

            result = _parse_json_response(response.text)

            if hasattr(response, "usage_metadata"):
                usage = response.usage_metadata
                print(f"  Resources tokens — input: {usage.prompt_token_count}, output: {usage.candidates_token_count}")

            return result
        except json.JSONDecodeError:
            if attempt == 0:
                print("  Resources JSON parse failed, retrying...")
                continue
            raise
        except Exception as e:
            if attempt == 0:
                print(f"  Resources error, retrying: {e}")
                continue
            raise

    return {"resources": []}
