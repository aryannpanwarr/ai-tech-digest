"""Entry point — orchestrates the full weekly digest pipeline."""

import asyncio
import sys

from dotenv import load_dotenv

from src.collectors.rss_collector import RSSCollector
from src.collectors.hackernews import HackerNewsCollector
from src.collectors.reddit import RedditCollector
from src.collectors.arxiv import ArxivCollector
from src.collectors.github_trending import GitHubTrendingCollector
from src.analysis.deduplicator import deduplicate
from src.analysis.analyzer import triage_articles, deep_analysis, curate_resources
from src.publisher.markdown_writer import write_post, update_resources
from src.publisher.git_publisher import git_publish
from src.config import RawArticle


async def collect_all_sources() -> list[RawArticle]:
    """Run all collectors concurrently and aggregate results."""
    collectors = [
        RSSCollector(),
        HackerNewsCollector(),
        RedditCollector(),
        ArxivCollector(),
        GitHubTrendingCollector(),
    ]

    tasks = [c.collect() for c in collectors]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles = []
    for i, result in enumerate(results):
        collector_name = collectors[i].__class__.__name__
        if isinstance(result, Exception):
            print(f"  {collector_name} failed: {result}")
        elif isinstance(result, list):
            all_articles.extend(result)
            print(f"  {collector_name}: {len(result)} articles")
        else:
            print(f"  {collector_name}: unexpected result type")

    return all_articles


async def run_pipeline():
    """Run the full weekly digest pipeline end-to-end."""
    load_dotenv()

    print("=" * 60)
    print("AI & Tech Weekly Digest Pipeline")
    print("=" * 60)

    # 1. Collect from all sources in parallel
    print("\n[1/7] Collecting articles...")
    articles = await collect_all_sources()
    print(f"Collected {len(articles)} total articles")

    if not articles:
        print("No articles collected. Exiting.")
        sys.exit(1)

    # 2. Deduplicate
    print("\n[2/7] Deduplicating...")
    unique = deduplicate(articles)
    print(f"Deduplicated to {len(unique)} unique articles")

    # 3. Triage with Gemini Flash
    print("\n[3/7] Triaging stories...")
    triage = await triage_articles(unique)
    num_stories = len(triage.get("stories", []))
    print(f"Identified {num_stories} top stories")

    if num_stories == 0:
        print("No stories identified. Exiting.")
        sys.exit(1)

    # 4. Deep analysis with Gemini Pro
    print("\n[4/7] Writing analysis...")
    analysis = await deep_analysis(triage, unique)
    print(f"Analysis generated: {len(analysis)} characters")

    # 5. Curate resources with Gemini Flash
    print("\n[5/7] Curating resources...")
    resources = await curate_resources(triage, unique)
    num_resources = len(resources.get("resources", []))
    print(f"Curated {num_resources} resources")

    # 6. Write markdown post and update resources.json
    print("\n[6/7] Publishing...")
    post_path = write_post(triage, analysis, resources, source_articles=unique)
    update_resources(resources)

    # 7. Git commit and push
    print("\n[7/7] Git publish...")
    git_publish()

    print("\n" + "=" * 60)
    print(f"Done! Published: {post_path}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_pipeline())
