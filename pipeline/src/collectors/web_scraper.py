"""Generic web scraper using crawl4ai for clean text extraction."""

import asyncio

from src.config import HTTP_TIMEOUT, MAX_RETRIES


async def scrape_url(url: str) -> str:
    """Scrape a URL and return clean markdown content.

    This is a utility used by other collectors, not a standalone collector.
    Uses crawl4ai for clean text extraction with retry logic.
    """
    for attempt in range(MAX_RETRIES + 1):
        try:
            from crawl4ai import AsyncWebCrawler

            async with AsyncWebCrawler() as crawler:
                result = await asyncio.wait_for(
                    crawler.arun(url=url),
                    timeout=HTTP_TIMEOUT,
                )
                if result and result.markdown:
                    return result.markdown[:50000]
                return ""
        except asyncio.TimeoutError:
            if attempt < MAX_RETRIES:
                await asyncio.sleep(2 ** attempt)
                continue
            print(f"Scraper timeout after {MAX_RETRIES + 1} attempts: {url}")
            return ""
        except ImportError:
            # crawl4ai not installed, fallback to basic httpx fetch
            return await _fallback_fetch(url)
        except Exception as e:
            if attempt < MAX_RETRIES:
                await asyncio.sleep(2 ** attempt)
                continue
            print(f"Scraper error for {url}: {e}")
            return ""
    return ""


async def _fallback_fetch(url: str) -> str:
    """Simple fallback using httpx if crawl4ai is not available."""
    import httpx

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            text = resp.text
            return text[:50000] if len(text) > 50000 else text
    except Exception as e:
        print(f"Fallback fetch error for {url}: {e}")
        return ""
