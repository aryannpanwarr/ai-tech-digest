# AI & Tech Weekly Digest — Agent Instructions

> **How to use this file:**
> - Tell Agent 1: "You are Agent 1. Read `/home/aryan/ai-tech-digest/agent.md` and follow ONLY the sections marked AGENT 1 and SHARED DATA CONTRACT."
> - Tell Agent 2: "You are Agent 2. Read `/home/aryan/ai-tech-digest/agent.md` and follow ONLY the sections marked AGENT 2 and SHARED DATA CONTRACT."
> - Agent 1 builds `pipeline/` — the Python backend that collects and analyzes news.
> - Agent 2 builds `website/` — the Next.js frontend that displays the digests.
> - Both agents write/read from `content/` using the shared data contract below.
> - **Neither agent should touch the other's directory.**

---

## PROJECT OVERVIEW

Build an autonomous website that:
- Scrapes high-quality AI and tech sources weekly
- Uses Google Gemini API to analyze, synthesize, and compile a comprehensive weekly digest
- Publishes to a static website automatically
- Provides curated, high-quality resources for readers
- Runs unattended via GitHub Actions cron scheduling

### Final Repository Structure

```
ai-tech-digest/
├── pipeline/                # AGENT 1 ONLY — Python backend
├── website/                 # AGENT 2 ONLY — Next.js frontend
├── content/                 # SHARED — both agents use this
│   ├── posts/               # Weekly digest markdown files
│   └── resources.json       # Cumulative resource index
├── .github/
│   └── workflows/
│       ├── weekly-digest.yml
│       └── deploy.yml
└── agent.md                 # This file
```

---

## SHARED DATA CONTRACT

**BOTH AGENTS MUST USE THESE EXACT FORMATS. DO NOT DEVIATE.**

### Post File Format: `content/posts/YYYY-MM-DD.md`

```markdown
---
title: "AI & Tech Weekly Digest — Week of March 1, 2026"
date: "2026-03-01"
week_number: 9
year: 2026
summary: "One paragraph TL;DR of the week's biggest stories."
top_stories:
  - title: "Story headline"
    category: "ai-research"
    significance: 9
    source_url: "https://example.com/article"
  - title: "Another story"
    category: "ai-industry"
    significance: 8
    source_url: "https://example.com/other"
categories:
  - ai-research
  - ai-industry
  - tech
  - open-source
  - policy
resources:
  - title: "Resource name"
    url: "https://example.com/resource"
    type: "paper"
    description: "Why this resource is worth your time."
---

Full post content in markdown here. Uses ## headings for sections.
```

**Frontmatter field rules:**
- `date`: ISO format YYYY-MM-DD, always a Sunday
- `week_number`: ISO week number (1-52)
- `category` values: ONLY one of `ai-research`, `ai-industry`, `tech`, `open-source`, `policy`
- `significance`: integer 1-10
- `type` values: ONLY one of `paper`, `article`, `tool`, `repo`, `video`, `podcast`, `newsletter`

### Resource Index Format: `content/resources.json`

```json
{
  "last_updated": "2026-03-01",
  "categories": {
    "newsletters": [
      {
        "name": "The Batch",
        "url": "https://www.deeplearning.ai/the-batch/",
        "description": "Andrew Ng's weekly AI newsletter.",
        "frequency": "weekly"
      }
    ],
    "podcasts": [],
    "youtube_channels": [],
    "blogs": [],
    "research_trackers": [],
    "tools": [],
    "communities": []
  }
}
```

### Sample Post for Testing

Agent 2 needs a sample post to develop against. Agent 1 should generate one, but if Agent 1 hasn't run yet, Agent 2 should create this exact file at `content/posts/2026-02-22.md`:

```markdown
---
title: "AI & Tech Weekly Digest — Week of February 22, 2026"
date: "2026-02-22"
week_number: 8
year: 2026
summary: "Google announces Gemini 2.5 Ultra, open-source AI agents gain traction, and the EU AI Act enforcement begins."
top_stories:
  - title: "Google Releases Gemini 2.5 Ultra"
    category: "ai-industry"
    significance: 9
    source_url: "https://blog.google/technology/ai/"
  - title: "Meta Open-Sources New Llama Architecture"
    category: "open-source"
    significance: 8
    source_url: "https://ai.meta.com/blog/"
  - title: "EU AI Act Compliance Deadline Hits"
    category: "policy"
    significance: 7
    source_url: "https://artificialintelligenceact.eu/"
categories:
  - ai-research
  - ai-industry
  - open-source
  - policy
resources:
  - title: "Gemini 2.5 Technical Report"
    url: "https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf"
    type: "paper"
    description: "The full technical report behind Google's latest model release."
  - title: "Awesome AI Agents"
    url: "https://github.com/e2b-dev/awesome-ai-agents"
    type: "repo"
    description: "Curated list of AI agent frameworks and tools."
  - title: "The Gradient Podcast"
    url: "https://thegradientpub.substack.com/"
    type: "podcast"
    description: "In-depth interviews with AI researchers."
---

## This Week in AI & Tech

> Google dropped Gemini 2.5 Ultra with state-of-the-art benchmarks, Meta continued its open-source blitz with a new Llama variant, and European companies scrambled to meet the first EU AI Act enforcement deadline. The theme this week: the gap between open and closed AI keeps narrowing.

## The Big Story

### Google Releases Gemini 2.5 Ultra

Google announced Gemini 2.5 Ultra, their most capable model to date. Key highlights include a 2 million token context window, native multimodal reasoning, and significant improvements in code generation benchmarks.

**Why it matters:** This puts direct competitive pressure on OpenAI and Anthropic. The 2M context window is particularly significant for enterprise document processing use cases.

**What comes next:** Expect rapid integration into Google Workspace and Cloud products over the coming weeks.

## Open Source & Tools

### Meta Open-Sources New Llama Architecture

Meta released a new Llama variant with mixture-of-experts architecture, achieving GPT-4 level performance at a fraction of the compute cost.

**Bottom Line:** Open-source models are now genuinely competitive with closed alternatives for most production use cases.

## Policy & Society

### EU AI Act Compliance Deadline Hits

February 2026 marks the first enforcement deadline for the EU AI Act. Companies deploying high-risk AI systems must now demonstrate compliance or face penalties up to 7% of global revenue.

**Bottom Line:** This is the beginning of real AI regulation with teeth. Companies operating in the EU need dedicated compliance infrastructure.

## Connecting the Dots

The convergence of more capable open models, increasing regulation, and fierce competition at the frontier suggests 2026 will be defined by **accessibility and accountability**. The technology is getting cheaper and more available, while the rules around its use are getting stricter and more concrete.
```

Also create a sample `content/resources.json`:

```json
{
  "last_updated": "2026-02-22",
  "categories": {
    "newsletters": [
      {
        "name": "The Batch",
        "url": "https://www.deeplearning.ai/the-batch/",
        "description": "Andrew Ng's weekly AI newsletter covering the most important developments.",
        "frequency": "weekly"
      },
      {
        "name": "Import AI",
        "url": "https://importai.substack.com/",
        "description": "Jack Clark's newsletter on AI policy and research.",
        "frequency": "weekly"
      }
    ],
    "podcasts": [
      {
        "name": "The Gradient Podcast",
        "url": "https://thegradientpub.substack.com/",
        "description": "In-depth interviews with AI researchers and practitioners.",
        "frequency": "weekly"
      }
    ],
    "youtube_channels": [],
    "blogs": [
      {
        "name": "Lilian Weng's Blog",
        "url": "https://lilianweng.github.io/",
        "description": "Thorough technical deep-dives into ML concepts by OpenAI researcher.",
        "frequency": "monthly"
      }
    ],
    "research_trackers": [
      {
        "name": "Papers With Code",
        "url": "https://paperswithcode.com/",
        "description": "Track state-of-the-art ML papers with their implementations.",
        "frequency": "daily"
      }
    ],
    "tools": [],
    "communities": [
      {
        "name": "r/MachineLearning",
        "url": "https://www.reddit.com/r/MachineLearning/",
        "description": "Reddit's main ML research discussion community.",
        "frequency": "daily"
      }
    ]
  }
}
```

---

## AGENT 1 INSTRUCTIONS — Backend Pipeline (Python)

**Your scope:** Build everything inside `pipeline/` and create the initial `content/` sample files.
**Do NOT touch:** `website/` directory.

### Directory Structure

```
pipeline/
├── pyproject.toml
├── .env.example
├── src/
│   ├── __init__.py
│   ├── main.py                # Entry point — orchestrates the full pipeline
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py            # Abstract base collector class
│   │   ├── rss_collector.py   # RSS feed collector
│   │   ├── hackernews.py      # HackerNews API collector
│   │   ├── reddit.py          # Reddit API collector
│   │   ├── arxiv.py           # ArXiv API collector
│   │   ├── github_trending.py # GitHub trending repos
│   │   └── web_scraper.py     # Generic URL scraper using crawl4ai
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── deduplicator.py    # Deduplicate stories across sources
│   │   ├── analyzer.py        # Gemini API calls for analysis
│   │   └── prompts.py         # All LLM prompt templates
│   ├── publisher/
│   │   ├── __init__.py
│   │   ├── markdown_writer.py # Generates markdown post matching data contract
│   │   └── git_publisher.py   # Git commit and push
│   └── config.py              # All configuration, source lists, constants
└── tests/
    ├── test_collectors.py
    ├── test_analysis.py
    └── test_publisher.py
```

### Step 1: Project Setup

Python 3.11+. Use `pyproject.toml`:

```toml
[project]
name = "ai-tech-digest-pipeline"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "google-genai>=1.0.0",
    "feedparser>=6.0",
    "httpx>=0.27",
    "crawl4ai>=0.4",
    "pydantic>=2.0",
    "python-dotenv>=1.0",
    "pyyaml>=6.0",
    "thefuzz>=0.22",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23"]
```

Create `.env.example`:
```
GEMINI_API_KEY=your_google_ai_studio_key_here
GITHUB_TOKEN=optional_for_higher_rate_limits
```

### Step 2: Build the Shared Data Model

In `src/config.py`, define the core data model used across all collectors:

```python
from pydantic import BaseModel
from datetime import datetime

class RawArticle(BaseModel):
    title: str
    url: str
    source: str              # e.g. "hackernews", "arxiv", "rss:techcrunch"
    content: str             # Full text or substantial excerpt
    published_at: datetime | None = None
    score: int | None = None # Upvotes, stars, etc.
    tags: list[str] = []
```

Also define all source configuration here: RSS feed URLs, subreddit lists, ArXiv categories, keywords for filtering, etc. Keep it in one place so it's easy to update.

### Step 3: Build Collectors

Each collector implements the same interface — an async function returning `list[RawArticle]`.

**Base class** (`collectors/base.py`):
```python
from abc import ABC, abstractmethod
from src.config import RawArticle

class BaseCollector(ABC):
    @abstractmethod
    async def collect(self) -> list[RawArticle]:
        pass
```

**RSS Collector** (`collectors/rss_collector.py`):
- Use `feedparser` to parse these feeds (store the list in `config.py`):
  - `https://techcrunch.com/feed/`
  - `https://www.theverge.com/rss/index.xml`
  - `https://feeds.arstechnica.com/arstechnica/technology-lab`
  - `https://blog.google/technology/ai/rss/`
  - `https://openai.com/blog/rss.xml`
  - `https://www.anthropic.com/rss.xml`
  - `https://huggingface.co/blog/feed.xml`
  - `https://simonwillison.net/atom/everything/`
  - `https://lilianweng.github.io/index.xml`
  - `https://newsletter.mlengineer.io/feed`
- Filter to articles from the last 7 days only
- Use `httpx` to fetch full article content from each URL
- Fallback to RSS summary if full fetch fails

**HackerNews Collector** (`collectors/hackernews.py`):
- Public API: `https://hacker-news.firebaseio.com/v0/`
- Fetch `/topstories.json` and `/beststories.json`
- For each story ID, fetch `/item/{id}.json`
- Filter: score > 50 AND title/URL contains AI/tech keywords
- Limit to top 30 stories to stay within rate limits
- Fetch linked article content with `httpx`

**Reddit Collector** (`collectors/reddit.py`):
- Use Reddit's public JSON API: append `.json` to any subreddit URL
- Subreddits: `MachineLearning`, `artificial`, `LocalLLaMA`, `technology`, `programming`
- Fetch `https://www.reddit.com/r/{sub}/top.json?t=week&limit=10`
- Collect: post title, selftext, URL, score, top 5 comments
- Set User-Agent header to avoid 429s

**ArXiv Collector** (`collectors/arxiv.py`):
- API: `http://export.arxiv.org/api/query`
- Query: `cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV`
- Parameters: `sortBy=submittedDate&sortOrder=descending&max_results=30`
- Collect: title, abstract, authors, arxiv URL, PDF link
- Content = abstract (don't fetch full PDFs)

**GitHub Trending** (`collectors/github_trending.py`):
- Use GitHub Search API: `https://api.github.com/search/repositories`
- Query: `stars:>50 pushed:>YYYY-MM-DD` (7 days ago) + AI/ML topic keywords
- Sort by stars
- Collect: repo name, description, stars, language, URL, README excerpt
- Use `GITHUB_TOKEN` if available for higher rate limits

**Web Scraper** (`collectors/web_scraper.py`):
- Generic scraper using `crawl4ai` for extracting clean text from any URL
- Returns markdown content
- Timeout: 15 seconds per URL
- Retry: 2 attempts with backoff
- This is a utility used by other collectors, not a standalone collector

### Step 4: Build Deduplicator

`analysis/deduplicator.py`:
- Normalize URLs (strip tracking params, www prefix, trailing slashes)
- Group articles with same normalized URL
- Use `thefuzz` library for fuzzy title matching (threshold: 80% similarity)
- When duplicates found: keep the version with the longest content
- Merge tags from all duplicate versions
- Return deduplicated `list[RawArticle]`

### Step 5: Build LLM Analyzer (Gemini API)

**Use the `google-genai` SDK** (the official Google Gen AI Python SDK).

`analysis/analyzer.py`:
```python
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Use **Gemini 2.5 Flash** (`gemini-2.5-flash-preview-05-20`) for triage and resource curation (fast, cheap).
Use **Gemini 2.5 Pro** (`gemini-2.5-pro-preview-05-06`) for the deep analysis pass (higher quality writing).

The pipeline chains 3 sequential LLM calls:

**Call 1 — Triage and Categorize** (Flash):

`analysis/prompts.py` — `TRIAGE_PROMPT`:
```
You are an expert AI and technology analyst. You will receive a JSON array
of articles, papers, and posts collected from various sources this past week.

Your job:
1. Identify the 8-15 most significant developments
2. Categorize each as exactly one of: ai-research, ai-industry, tech, open-source, policy
3. Rate significance 1-10 (10 = paradigm shifting, 7+ = major, 4-6 = notable)
4. Group articles covering the same story by referencing their indices

Respond with ONLY valid JSON, no markdown fencing:
{
  "stories": [
    {
      "headline": "Short punchy headline",
      "category": "ai-research",
      "significance": 8,
      "source_article_indices": [0, 3, 7],
      "one_line_summary": "One sentence on what happened."
    }
  ]
}
```

**Call 2 — Deep Analysis** (Pro):

`ANALYSIS_PROMPT`:
```
You are writing the weekly AI & Tech Digest. You will receive the triaged
top stories along with their full source material.

Write a comprehensive, thorough analysis. Requirements:
- Clear, authoritative, and engaging tone
- For each story: WHAT happened, WHY it matters, WHAT COMES NEXT
- Draw connections between stories where they exist
- Include specific technical details — never be vague
- Organize into sections by category
- End each section with a "Bottom Line" takeaway
- Be opinionated where warranted — readers want analysis, not summaries
- Length: 2000-4000 words
- Use markdown: ## headings, bullet points, **bold** for emphasis

Required structure (use these exact headings):

## This Week in AI & Tech
> One paragraph executive summary of the entire week

## The Big Story
[The single most important development, with deep analysis]

## AI Research & Breakthroughs
[Papers, new techniques, benchmark results. Skip if nothing notable.]

## Industry Moves
[Product launches, funding, acquisitions, partnerships. Skip if nothing notable.]

## Open Source & Tools
[New repos, framework updates, community projects. Skip if nothing notable.]

## Policy & Society
[Regulation, ethics, societal impact. Skip if nothing notable.]

## Connecting the Dots
[Cross-cutting analysis: what these stories mean together, emerging trends]
```

**Call 3 — Resource Curation** (Flash):

`RESOURCES_PROMPT`:
```
Given the articles and analysis from this week, recommend 5-10 high-quality
resources for readers who want to go deeper.

Resource quality criteria:
- Primary sources preferred (original papers, official announcements — NOT re-blogs)
- Evergreen learning resources relevant to this week's themes
- Tools or repos readers can actually use today
- Long-form analysis from recognized domain experts

For each, explain in 1-2 sentences WHY it's worth the reader's time.

Respond with ONLY valid JSON, no markdown fencing:
{
  "resources": [
    {
      "title": "Name of the resource",
      "url": "https://actual-url.com",
      "type": "paper|article|tool|repo|video|podcast|newsletter",
      "description": "Why this is worth reading."
    }
  ]
}
```

**Implementation notes for `analyzer.py`:**
- Parse JSON responses with error handling — if JSON parsing fails, retry the call once
- Set `temperature=0.3` for triage, `temperature=0.7` for analysis, `temperature=0.3` for resources
- Set reasonable `max_output_tokens`: 2000 for triage, 8000 for analysis, 2000 for resources
- Log token usage for cost tracking
- Total input per run will be large (all collected articles) — Gemini's 1M context window handles this

### Step 6: Build Publisher

**`publisher/markdown_writer.py`:**
- Takes triage results, analysis text, and curated resources
- Builds YAML frontmatter matching the SHARED DATA CONTRACT exactly
- Writes to `content/posts/YYYY-MM-DD.md` where the date is the current Sunday
- Updates `content/resources.json`: merge new resources into existing file, don't overwrite
- Use `pyyaml` for frontmatter serialization

**`publisher/git_publisher.py`:**
- Uses `subprocess` to run git commands
- `git add content/`
- `git commit -m "digest: Week {week_number}, {year}"`
- `git push origin main`
- Handle case where there are no changes (exit cleanly)

### Step 7: Main Orchestrator

**`src/main.py`:**
```python
import asyncio
from dotenv import load_dotenv

async def run_pipeline():
    load_dotenv()

    # 1. Collect from all sources in parallel
    print("Collecting articles...")
    articles = await collect_all_sources()
    print(f"Collected {len(articles)} articles")

    # 2. Deduplicate
    print("Deduplicating...")
    unique = deduplicate(articles)
    print(f"Deduplicated to {len(unique)} unique articles")

    # 3. Triage with Gemini Flash
    print("Triaging stories...")
    triage = await triage_articles(unique)
    print(f"Identified {len(triage['stories'])} top stories")

    # 4. Deep analysis with Gemini Pro
    print("Writing analysis...")
    analysis = await deep_analysis(triage, unique)

    # 5. Curate resources with Gemini Flash
    print("Curating resources...")
    resources = await curate_resources(triage, unique)

    # 6. Write markdown post and update resources.json
    print("Publishing...")
    post_path = write_post(triage, analysis, resources)
    update_resources(resources)

    # 7. Git commit and push
    git_publish()

    print(f"Done! Published: {post_path}")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
```

- Run all collectors concurrently with `asyncio.gather` (with `return_exceptions=True` so one failing source doesn't kill the pipeline)
- Log everything to stdout (GitHub Actions captures it)
- Exit with code 1 on fatal errors so the GitHub Action fails visibly

### Step 8: Write Tests

- `test_collectors.py`: Mock HTTP responses, verify each collector returns valid `RawArticle` objects
- `test_analysis.py`: Mock Gemini API responses, verify JSON parsing and error handling
- `test_publisher.py`: Verify markdown output matches the data contract format exactly
- Use `pytest` and `pytest-asyncio`

### Step 9: Create Initial Content Files

Create the sample `content/posts/2026-02-22.md` and `content/resources.json` files as specified in the SHARED DATA CONTRACT section above. These are needed for Agent 2 to develop against.

### Step 10: Create GitHub Actions Workflows

**`.github/workflows/weekly-digest.yml`:**
```yaml
name: Weekly Digest Pipeline

on:
  schedule:
    - cron: '0 14 * * 0'    # Every Sunday at 2 PM UTC
  workflow_dispatch:          # Manual trigger for testing

jobs:
  generate-digest:
    runs-on: ubuntu-latest
    permissions:
      contents: write        # Needed to push commits
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: cd pipeline && pip install -e ".[dev]"

      - name: Install Playwright for crawl4ai
        run: playwright install chromium

      - name: Run pipeline
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: cd pipeline && python -m src.main

      - name: Commit and push new digest
        run: |
          git config user.name "AI Digest Bot"
          git config user.email "bot@ai-digest.dev"
          git add content/
          git diff --staged --quiet || git commit -m "digest: Week $(date +%V), $(date +%Y)"
          git push
```

**`.github/workflows/deploy.yml`:**
```yaml
name: Deploy Website

on:
  push:
    branches: [main]
    paths:
      - 'website/**'
      - 'content/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install and build
        run: cd website && npm ci && npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./website
```

---

## AGENT 2 INSTRUCTIONS — Frontend Website (Next.js)

**Your scope:** Build everything inside `website/`. Also create `content/` with the sample files from the SHARED DATA CONTRACT if they don't exist yet.
**Do NOT touch:** `pipeline/` directory.

### Directory Structure

```
website/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── public/
│   ├── favicon.ico
│   └── og-image.png
├── src/
│   ├── app/
│   │   ├── layout.tsx               # Root layout: nav, footer, fonts, theme
│   │   ├── page.tsx                 # Homepage: latest digest + archive
│   │   ├── digest/
│   │   │   └── [slug]/
│   │   │       └── page.tsx         # Individual digest post
│   │   ├── resources/
│   │   │   └── page.tsx             # Curated resources page
│   │   ├── about/
│   │   │   └── page.tsx             # About the project
│   │   └── feed.xml/
│   │       └── route.ts             # RSS feed endpoint
│   ├── components/
│   │   ├── Header.tsx               # Site header with nav
│   │   ├── Footer.tsx               # Site footer
│   │   ├── DigestCard.tsx           # Digest preview for archive listing
│   │   ├── StoryCard.tsx            # Story item within a digest
│   │   ├── ResourceCard.tsx         # Resource item display
│   │   ├── SignificanceBadge.tsx    # 1-10 visual indicator
│   │   ├── CategoryTag.tsx          # Colored category pill
│   │   ├── TableOfContents.tsx      # Sticky sidebar TOC
│   │   ├── SearchBar.tsx            # Search past digests
│   │   ├── ThemeToggle.tsx          # Dark/light mode switch
│   │   └── ShareButtons.tsx         # Twitter/X, LinkedIn, copy link
│   ├── lib/
│   │   ├── posts.ts                 # Read & parse content/posts/*.md
│   │   ├── resources.ts             # Read & parse content/resources.json
│   │   └── utils.ts                 # Reading time calc, date formatting
│   └── styles/
│       └── globals.css              # Tailwind base + custom styles
```

### Step 1: Project Setup

Initialize with:
```bash
npx create-next-app@latest website --typescript --tailwind --app --src-dir
```

Dependencies to install:
```
gray-matter              # Parse YAML frontmatter from markdown
react-markdown           # Render markdown to React components
remark-gfm              # GitHub-flavored markdown (tables, strikethrough)
rehype-highlight         # Syntax highlighting for code blocks
rehype-slug              # Add IDs to headings (for TOC linking)
date-fns                 # Date formatting
```

Tailwind config:
- Font: `Inter` for body, `JetBrains Mono` for code
- Dark mode: `class` strategy (for toggle control)
- Content max-width: `prose` class with `max-w-3xl` for article content
- Color tokens for categories:
  - ai-research: `purple-500/600`
  - ai-industry: `blue-500/600`
  - tech: `emerald-500/600`
  - open-source: `orange-500/600`
  - policy: `rose-500/600`

### Step 2: Content Parsing Library

**`lib/posts.ts`** — This is the bridge between pipeline output and the website:

```typescript
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const POSTS_DIR = path.join(process.cwd(), '..', 'content', 'posts');

export interface TopStory {
  title: string;
  category: 'ai-research' | 'ai-industry' | 'tech' | 'open-source' | 'policy';
  significance: number;
  source_url: string;
}

export interface Resource {
  title: string;
  url: string;
  type: 'paper' | 'article' | 'tool' | 'repo' | 'video' | 'podcast' | 'newsletter';
  description: string;
}

export interface DigestPost {
  slug: string;
  title: string;
  date: string;
  weekNumber: number;
  year: number;
  summary: string;
  topStories: TopStory[];
  categories: string[];
  resources: Resource[];
  content: string;
  readingTime: number;      // Calculated from word count
}

export function getAllPosts(): DigestPost[] {
  // 1. Read all .md files from POSTS_DIR
  // 2. Parse frontmatter with gray-matter
  // 3. Calculate reading time (words / 200)
  // 4. Sort by date descending (newest first)
  // 5. Return array
}

export function getPostBySlug(slug: string): DigestPost | null {
  // slug = "2026-02-22" (the filename without .md)
}

export function getAdjacentPosts(slug: string): { prev: DigestPost | null; next: DigestPost | null } {
  // For prev/next navigation on digest pages
}
```

**`lib/resources.ts`:**
```typescript
const RESOURCES_PATH = path.join(process.cwd(), '..', 'content', 'resources.json');

export interface ResourceEntry {
  name: string;
  url: string;
  description: string;
  frequency?: string;
}

export interface ResourceIndex {
  last_updated: string;
  categories: Record<string, ResourceEntry[]>;
}

export function getResources(): ResourceIndex {
  // Read and parse content/resources.json
}
```

**`lib/utils.ts`:**
```typescript
export function calculateReadingTime(content: string): number {
  return Math.ceil(content.split(/\s+/).length / 200);
}

export function formatDate(dateStr: string): string {
  // Return "February 22, 2026" format
}
```

### Step 3: Build Pages

**Root Layout (`app/layout.tsx`):**
- Import Inter and JetBrains Mono from `next/font/google`
- `<html>` with `suppressHydrationWarning` for dark mode
- Inline script to check localStorage for theme preference (prevents flash)
- `<Header />` and `<Footer />` wrapping `{children}`
- Meta: site title "AI & Tech Weekly Digest", description, OG image

**Homepage (`app/page.tsx`):**
- Hero section:
  - Site name in large bold text
  - Tagline: "Your weekly deep-dive into AI & technology"
  - Subtext: "Autonomously curated. Thoroughly analyzed. Every Sunday."
- Latest digest section:
  - The newest post displayed prominently
  - Show: title, date, summary, top 3 stories with significance badges
  - Large "Read this week's digest" CTA button
- Archive section:
  - Grid/list of past digest `<DigestCard />`s
  - Show all past posts, newest first

**Digest Page (`app/digest/[slug]/page.tsx`):**
- Use `generateStaticParams` to pre-render all digest pages
- Two-column layout on desktop: main content (left) + sticky TOC (right)
- Top section before article content:
  - Title, date, reading time
  - Category tags for this week's stories
  - Top stories as `<StoryCard />` items (collapsible on mobile)
- Main content: render markdown with `react-markdown` + `remark-gfm` + `rehype-highlight` + `rehype-slug`
- After content:
  - "Resources from this week" section showing post's resources as `<ResourceCard />`s
  - Previous / Next digest navigation links
  - Share buttons
- Generate `<head>` metadata: title, description (from summary), OG tags

**Resources Page (`app/resources/page.tsx`):**
- Read from `content/resources.json`
- Group by category with collapsible sections
- Each category: heading + grid of `<ResourceCard />`s
- Show `last_updated` date at the top
- Simple client-side search/filter bar

**About Page (`app/about/page.tsx`):**
- What this site is: "An autonomous AI-powered weekly digest of AI and technology news"
- How it works: brief pipeline description (sources → collection → AI analysis → publish)
- Data sources: list the RSS feeds, APIs used
- Transparency: "Analysis is generated using Google's Gemini AI models"
- Open source: link to the GitHub repo

**RSS Feed (`app/feed.xml/route.ts`):**
- Route handler that returns XML with `Content-Type: application/xml`
- Include all posts: title, link, pubDate, description (summary)
- Channel metadata: site title, description, link

### Step 4: Build Components

**`Header.tsx`:**
- Site name/logo (text-based, no image needed) linking to `/`
- Nav links: Digest, Resources, About
- `<ThemeToggle />` on the right
- Sticky on scroll, with backdrop blur
- Mobile: hamburger menu or simplified layout

**`Footer.tsx`:**
- "Powered by Gemini AI" with link to the project's about page
- RSS feed link
- GitHub repo link
- Current year

**`DigestCard.tsx`:** (used on homepage archive)
- Props: `post: DigestPost`
- Card with: formatted date, title, summary (truncated to 2 lines)
- Show top 3 category tags as `<CategoryTag />`
- Entire card is a link to `/digest/{slug}`
- Subtle hover effect

**`StoryCard.tsx`:** (used on digest page top section)
- Props: `story: TopStory`
- Horizontal layout: `<SignificanceBadge />` + title + `<CategoryTag />`
- Title links to `source_url` (external link, opens in new tab)

**`ResourceCard.tsx`:**
- Props: `resource: Resource`
- Card with: title (links to URL), type badge, description
- Subtle border, clean layout

**`SignificanceBadge.tsx`:**
- Props: `score: number`
- Visual display:
  - 9-10: Red dot/badge, label "Critical"
  - 7-8: Orange dot/badge, label "Major"
  - 4-6: Blue dot/badge, label "Notable"
  - 1-3: Gray dot/badge, label "Minor"
- Small, non-distracting — a colored circle with the number inside

**`CategoryTag.tsx`:**
- Props: `category: string`
- Colored pill/chip using the color mapping:
  - `ai-research` → purple
  - `ai-industry` → blue
  - `tech` → emerald/green
  - `open-source` → orange
  - `policy` → rose/red
- Rounded, small text, consistent sizing

**`TableOfContents.tsx`:**
- Extract `##` and `###` headings from the markdown content
- Generate anchor links using heading IDs (from `rehype-slug`)
- Sticky position on desktop (top: 100px, max-height: calc(100vh - 200px), overflow-y: auto)
- Highlight the current section using Intersection Observer
- On mobile: hide by default, show as a floating button that opens a drawer/modal

**`ThemeToggle.tsx`:**
- Sun/moon icon button
- Toggle `dark` class on `<html>` element
- Persist choice in `localStorage`

**`ShareButtons.tsx`:**
- Props: `title: string, url: string`
- Buttons for: Twitter/X (pre-filled tweet), LinkedIn, Copy Link
- Copy Link shows brief "Copied!" feedback

**`SearchBar.tsx`:**
- Client-side search across post titles, summaries, and story headlines
- Debounced input
- Show results as a dropdown with links to matching digests

### Step 5: Design Specifications

The site should feel like a premium editorial publication — think Stratechery, The Pragmatic Engineer, or Daring Fireball.

**Typography:**
- Body: 18px/1.7 line-height for articles, 16px for UI elements
- Headings: bold, tight line-height, clear size hierarchy
- Code: JetBrains Mono, slightly smaller than body

**Colors (light mode):**
- Background: `#ffffff`
- Text: `#111827` (gray-900)
- Secondary text: `#6b7280` (gray-500)
- Borders: `#e5e7eb` (gray-200)
- Accent: category colors only

**Colors (dark mode):**
- Background: `#0f172a` (slate-900)
- Text: `#f1f5f9` (slate-100)
- Secondary text: `#94a3b8` (slate-400)
- Borders: `#334155` (slate-700)
- Accent: same category colors, slightly adjusted for contrast

**Layout:**
- Article content: max-width 720px, centered
- With TOC sidebar: max-width 1100px (720px content + 300px TOC + gap)
- Generous padding: 24px mobile, 48px desktop
- Cards: subtle border, no heavy shadows

**Responsive breakpoints:**
- Mobile: < 768px — single column, no TOC sidebar, hamburger nav
- Tablet: 768px-1024px — single column, TOC as collapsible
- Desktop: > 1024px — full layout with sidebar TOC

### Step 6: Static Generation & SEO

- Every page should be statically generated at build time
- `generateStaticParams` on digest/[slug] page
- `generateMetadata` on every page for proper `<head>` tags:
  - `title`: "Post Title | AI & Tech Weekly Digest"
  - `description`: from post summary
  - `openGraph`: title, description, type, image
  - `twitter`: card, title, description
- Add JSON-LD structured data (Article schema) on digest pages
- Generate `sitemap.xml` using Next.js built-in sitemap generation

### Step 7: Important Implementation Notes

- The `content/` directory is at `../content/` relative to `website/`. Configure path resolution accordingly in `next.config.ts` if needed.
- If `content/posts/` is empty or doesn't exist, the homepage should show a friendly "No digests yet — check back Sunday!" message, not crash.
- All external links (`source_url` in stories, resource URLs) should open in new tabs with `rel="noopener noreferrer"`.
- Images are not expected in the markdown content — don't build image handling.
- The site must work as a static export. Avoid any server-only features except the route handlers for RSS.

---

## ENVIRONMENT SECRETS (for deployment)

Set in GitHub repo → Settings → Secrets and Variables → Actions:

| Secret | Required | Used By |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Pipeline (Gemini API) |
| `GITHUB_TOKEN` | Auto | Pipeline (GitHub API), Actions (git push) |
| `VERCEL_TOKEN` | Yes | Deploy workflow |
| `VERCEL_ORG_ID` | Yes | Deploy workflow |
| `VERCEL_PROJECT_ID` | Yes | Deploy workflow |

---

## QUALITY CHECKLIST

### Agent 1 must verify:
- [ ] `pip install -e .` works cleanly
- [ ] Each collector runs without errors (test individually)
- [ ] Deduplication reduces article count
- [ ] Gemini API calls succeed and return valid JSON
- [ ] Generated markdown file matches the SHARED DATA CONTRACT exactly
- [ ] `resources.json` is valid JSON matching the contract
- [ ] `main.py` runs end-to-end and produces a post in `content/posts/`
- [ ] Pipeline doesn't crash if one collector fails (graceful degradation)
- [ ] All tests pass

### Agent 2 must verify:
- [ ] `npm run dev` starts without errors
- [ ] Homepage renders with the sample post
- [ ] Digest page renders markdown correctly with TOC
- [ ] Resources page displays grouped resources
- [ ] Dark mode toggle works without flash of wrong theme
- [ ] Mobile layout is usable (test at 375px width)
- [ ] `npm run build` succeeds (static generation works)
- [ ] RSS feed returns valid XML
- [ ] All links work, external links open in new tabs
- [ ] Category tags show correct colors
- [ ] Significance badges show correct colors and labels
