"""Deduplicate articles across sources using URL normalization and fuzzy title matching."""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from thefuzz import fuzz

from src.config import RawArticle

# URL parameters commonly used for tracking that should be stripped
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "ref", "source", "fbclid", "gclid", "mc_cid", "mc_eid",
}

FUZZY_TITLE_THRESHOLD = 80


def normalize_url(url: str) -> str:
    """Normalize a URL by stripping tracking params, www prefix, and trailing slashes."""
    try:
        parsed = urlparse(url)

        # Strip www prefix
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]

        # Strip tracking parameters
        query_params = parse_qs(parsed.query)
        cleaned_params = {
            k: v for k, v in query_params.items() if k.lower() not in TRACKING_PARAMS
        }
        cleaned_query = urlencode(cleaned_params, doseq=True)

        # Strip trailing slashes from path
        path = parsed.path.rstrip("/")

        # Reconstruct
        normalized = urlunparse((
            parsed.scheme.lower(),
            netloc,
            path,
            parsed.params,
            cleaned_query,
            "",  # drop fragment
        ))
        return normalized
    except Exception:
        return url.lower().rstrip("/")


def deduplicate(articles: list[RawArticle]) -> list[RawArticle]:
    """Deduplicate articles by URL and fuzzy title matching.

    Strategy:
    1. Group by normalized URL — exact URL matches are definite duplicates.
    2. Within remaining articles, use fuzzy title matching to find duplicates.
    3. When duplicates found: keep the version with the longest content.
    4. Merge tags from all duplicate versions.
    """
    if not articles:
        return []

    # Phase 1: Group by normalized URL
    url_groups: dict[str, list[RawArticle]] = {}
    for article in articles:
        norm_url = normalize_url(article.url)
        if norm_url not in url_groups:
            url_groups[norm_url] = []
        url_groups[norm_url].append(article)

    # Merge URL-based duplicates
    merged: list[RawArticle] = []
    for group in url_groups.values():
        merged.append(_merge_group(group))

    # Phase 2: Fuzzy title matching on the merged results
    used = set()
    final: list[RawArticle] = []

    for i, article in enumerate(merged):
        if i in used:
            continue

        group = [article]
        for j in range(i + 1, len(merged)):
            if j in used:
                continue
            similarity = fuzz.token_sort_ratio(article.title, merged[j].title)
            if similarity >= FUZZY_TITLE_THRESHOLD:
                group.append(merged[j])
                used.add(j)

        used.add(i)
        final.append(_merge_group(group))

    return final


def _merge_group(group: list[RawArticle]) -> RawArticle:
    """Merge a group of duplicate articles, keeping the longest content and merging tags."""
    if len(group) == 1:
        return group[0]

    # Keep the version with the longest content
    best = max(group, key=lambda a: len(a.content))

    # Merge all tags
    all_tags = set()
    for article in group:
        all_tags.update(article.tags)

    # Keep the highest score
    best_score = max((a.score for a in group if a.score is not None), default=None)

    return RawArticle(
        title=best.title,
        url=best.url,
        source=best.source,
        content=best.content,
        published_at=best.published_at,
        score=best_score,
        tags=list(all_tags),
    )
