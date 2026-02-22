# AI & Tech Weekly Digest — Full Build Instructions

## Project Overview

Build an autonomous website that:
- Scrapes high-quality AI and tech sources weekly
- Uses Claude API to analyze, synthesize, and compile a comprehensive weekly digest post
- Publishes to a static website automatically
- Provides curated, high-quality resources for readers
- Runs entirely unattended via cron scheduling

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    WEEKLY CRON JOB                       │
│              (GitHub Actions / Vercel Cron)              │
└─────────────┬───────────────────────────────┬───────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│   1. DATA COLLECTION    │     │   (runs sequentially)   │
│                         │     │                         │
│  - RSS feeds            │     │                         │
│  - HackerNews API       │     │                         │
│  - Reddit API           │     │                         │
│  - ArXiv API            │     │                         │
│  - GitHub Trending      │     │                         │
│  - Tech news sites      │     │                         │
│    (via Crawl4AI)       │     │                         │
└────────────┬────────────┘     │                         │
             │                  │                         │
             ▼                  │                         │
┌─────────────────────────┐     │                         │
│   2. LLM ANALYSIS       │     │                         │
│   (Claude API)          │     │                         │
│                         │     │                         │
│  - Deduplicate stories  │     │                         │
│  - Rank by significance │     │                         │
│  - Categorize           │     │                         │
│  - Synthesize trends    │     │                         │
│  - Generate weekly post │     │                         │
│  - Curate resources     │     │                         │
└────────────┬────────────┘     │                         │
             │                  │                         │
             ▼                  │                         │
┌─────────────────────────┐     │                         │
│   3. PUBLISH            │     │                         │
│                         │     │                         │
│  - Write markdown + JSON│     │                         │
│  - Git commit & push    │     │                         │
│  - Site rebuilds via CI │     │                         │
└─────────────────────────┘     └─────────────────────────┘
```

---

## Shared Data Contract

**IMPORTANT: Both agents must use this exact format.**

### Post File: `content/posts/YYYY-MM-DD.md`

```markdown
---
title: "AI & Tech Weekly Digest — Week of March 1, 2026"
date: "2026-03-01"
week_number: 9
year: 2026
summary: "One paragraph TL;DR of the week's biggest stories."
top_stories:
  - title: "Story headline"
    category: "ai-research | ai-industry | tech | open-source | policy"
    significance: 9
    source_url: "https://..."
  - title: "Another story"
    category: "ai-research"
    significance: 8
    source_url: "https://..."
categories:
  - ai-research
  - ai-industry
  - tech
  - open-source
  - policy
resources:
  - title: "Resource name"
    url: "https://..."
    type: "paper | article | tool | repo | video | podcast | newsletter"
    description: "Why this resource is worth your time."
  - title: "Another resource"
    url: "https://..."
    type: "repo"
    description: "Description here."
---

<!-- Full post content in markdown below -->
```

### Resource Index: `content/resources.json`

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
    "communities": []
  }
}
```

---

## AGENT 1 INSTRUCTIONS — Backend Pipeline (Python)

### Directory Structure

```
pipeline/
├── pyproject.toml
├── .env.example
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point, orchestrates the full pipeline
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract base collector
│   │   ├── rss_collector.py  # RSS feed collector
│   │   ├── hackernews.py     # HackerNews API collector
│   │   ├── reddit.py         # Reddit API collector
│   │   ├── arxiv.py          # ArXiv API collector
│   │   ├── github_trending.py# GitHub trending repos
│   │   └── web_scraper.py    # Generic web scraper using Crawl4AI
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── deduplicator.py   # Remove duplicate stories across sources
│   │   ├── analyzer.py       # Claude API calls for analysis
│   │   └── prompts.py        # All LLM prompt templates
│   ├── publisher/
│   │   ├── __init__.py
│   │   ├── markdown_writer.py# Generates the markdown post file
│   │   └── git_publisher.py  # Commits and pushes to repo
│   └── config.py             # Configuration and source definitions
└── tests/
    ├── test_collectors.py
    ├── test_analysis.py
    └── test_publisher.py
```

### Step-by-Step Build Instructions

#### Step 1: Project Setup

- Use Python 3.11+
- Use `pyproject.toml` with these dependencies:
  ```
  anthropic          # Claude API
  feedparser         # RSS parsing
  httpx              # HTTP client (async)
  crawl4ai           # Web scraping with JS rendering
  pydantic           # Data validation
  python-dotenv      # Environment variables
  pyyaml             # YAML frontmatter generation
  ```
- Create `.env.example` with:
  ```
  ANTHROPIC_API_KEY=your_key_here
  REDDIT_CLIENT_ID=optional
  REDDIT_CLIENT_SECRET=optional
  GITHUB_TOKEN=optional
  ```

#### Step 2: Build Collectors

Each collector must return a list of `RawArticle` objects:

```python
from pydantic import BaseModel
from datetime import datetime

class RawArticle(BaseModel):
    title: str
    url: str
    source: str            # e.g., "hackernews", "arxiv", "rss:techcrunch"
    content: str           # Full text or substantial excerpt
    published_at: datetime | None
    score: int | None      # Upvotes, stars, etc. (if available)
    tags: list[str]        # Any available tags/categories
```

**RSS Collector** (`rss_collector.py`):
- Use `feedparser` to parse these feeds (and make the list configurable):
  - https://techcrunch.com/feed/
  - https://www.theverge.com/rss/index.xml
  - https://feeds.arstechnica.com/arstechnica/technology-lab
  - https://blog.google/technology/ai/rss/
  - https://openai.com/blog/rss.xml
  - https://www.anthropic.com/rss.xml
  - https://huggingface.co/blog/feed.xml
  - https://simonwillison.net/atom/everything/
  - https://lilianweng.github.io/index.xml
- Filter to only articles from the last 7 days
- Use `crawl4ai` or `httpx` to fetch full article content from each URL

**HackerNews Collector** (`hackernews.py`):
- Use the public API: https://hacker-news.firebaseio.com/v0/
- Fetch top stories and best stories
- Filter to AI/tech related posts (score > 50, relevant keywords)
- Fetch full content from linked URLs using `crawl4ai`

**Reddit Collector** (`reddit.py`):
- Scrape or use Reddit's JSON API (append `.json` to subreddit URLs)
- Subreddits: r/MachineLearning, r/artificial, r/LocalLLaMA, r/technology, r/programming
- Filter to top posts of the week (score > 100)
- Collect post text + top comments for discussion context

**ArXiv Collector** (`arxiv.py`):
- Use the ArXiv API: http://export.arxiv.org/api/query
- Search categories: cs.AI, cs.LG, cs.CL, cs.CV
- Sort by submission date, last 7 days
- Collect title, abstract, authors, PDF link

**GitHub Trending** (`github_trending.py`):
- Scrape https://github.com/trending?since=weekly
- Or use the GitHub API to search repos created/updated this week with high star counts
- Filter to AI/ML related repos
- Collect: repo name, description, stars, language, URL

**Web Scraper** (`web_scraper.py`):
- Generic scraper using `crawl4ai` for any URL
- Returns clean markdown content
- Handles JS-rendered pages
- Has retry logic and timeout handling

#### Step 3: Build Deduplicator

- Use simple heuristics first: URL normalization, title similarity (fuzzy matching)
- Group articles that cover the same story/event
- Keep the highest-quality version (longest content, most reputable source)
- Merge metadata (combine tags, keep all source URLs)

#### Step 4: Build LLM Analyzer

This is the core of the project. Use the Anthropic Python SDK.

**`prompts.py`** — Define these prompt templates:

**Prompt 1: Triage and Categorize**
```
You are an expert AI and technology analyst. You will receive a collection
of articles, papers, and posts from the past week.

Your job:
1. Identify the most significant developments (aim for 8-15 top stories)
2. Categorize each into: ai-research, ai-industry, tech, open-source, policy
3. Rate significance 1-10 (10 = paradigm shifting, 7+ = major, 4-6 = notable)
4. Group articles that cover the same story

Output as JSON:
{
  "stories": [
    {
      "headline": "...",
      "category": "...",
      "significance": 8,
      "source_articles": [0, 3, 7],  // indices of input articles
      "one_line_summary": "..."
    }
  ]
}
```

**Prompt 2: Deep Analysis**
```
You are writing the weekly AI & Tech Digest. Given these top stories with
their source material, write a comprehensive analysis.

Requirements:
- Write in a clear, authoritative, and engaging tone
- For each story, explain WHAT happened, WHY it matters, and WHAT COMES NEXT
- Draw connections between stories where they exist
- Include specific technical details — do not be vague
- Organize into sections by category
- End each section with a "Bottom Line" takeaway
- Be opinionated where warranted — readers want analysis, not just summaries
- Total length: 2000-4000 words
- Use markdown formatting with headers, bullet points, and bold for emphasis

Structure:
## This Week in AI & Tech
> One paragraph executive summary

## The Big Story
[The single most significant development of the week, with deep analysis]

## AI Research & Breakthroughs
[Academic papers, new techniques, benchmark results]

## Industry Moves
[Product launches, funding, acquisitions, partnerships]

## Open Source & Tools
[New repos, framework updates, community projects]

## Policy & Society
[Regulation, ethics, societal impact — only if notable events occurred]

## Connecting the Dots
[Cross-cutting trends, what these stories mean together]
```

**Prompt 3: Resource Curation**
```
Given the articles and analysis from this week, recommend 5-10 high-quality
resources for readers who want to go deeper. These should be:
- Primary sources (original papers, official announcements, not re-blogs)
- Evergreen learning resources relevant to this week's themes
- Tools or repos readers can actually use
- Thoughtful long-form analysis from domain experts

For each resource, explain in 1-2 sentences WHY it's worth the reader's time.

Output as JSON matching this schema:
{
  "resources": [
    {
      "title": "...",
      "url": "...",
      "type": "paper|article|tool|repo|video|podcast|newsletter",
      "description": "..."
    }
  ]
}
```

**`analyzer.py`** — Implementation:
- Use `anthropic` SDK with `claude-sonnet-4-20250514` (good balance of quality and cost)
- For the deep analysis prompt, use `claude-opus-4-20250115` for higher quality
- Pass all collected articles as context (use prompt caching for the system prompt)
- Chain the three prompts sequentially: triage → analysis → resources
- Parse JSON outputs with error handling and retry logic
- Total cost should be ~$1-3 per weekly run

#### Step 5: Build Publisher

**`markdown_writer.py`**:
- Take the analysis output and format it as the markdown file specified in the data contract
- Generate proper YAML frontmatter with all metadata
- Write to `content/posts/YYYY-MM-DD.md`
- Update `content/resources.json` with new resources (merge, don't overwrite)

**`git_publisher.py`**:
- Stage the new/modified files
- Commit with message: "digest: Week N, YYYY"
- Push to the configured remote branch
- Use `subprocess` or `gitpython`

#### Step 6: Main Orchestrator

**`main.py`**:
```python
async def run_pipeline():
    # 1. Collect from all sources in parallel
    articles = await collect_all_sources()

    # 2. Deduplicate
    unique_articles = deduplicate(articles)

    # 3. Analyze with Claude
    triage = await triage_articles(unique_articles)
    analysis = await deep_analysis(triage, unique_articles)
    resources = await curate_resources(triage, unique_articles)

    # 4. Generate markdown
    post_path = write_post(analysis, resources, triage)

    # 5. Publish
    git_publish(post_path)

    print(f"Published: {post_path}")
```

#### Step 7: Write Tests

- Test each collector with mocked HTTP responses
- Test deduplicator with known duplicate sets
- Test markdown writer output format matches the data contract
- Test the full pipeline with a small set of fixture data

---

## AGENT 2 INSTRUCTIONS — Frontend Website (Next.js)

### Directory Structure

```
website/
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── public/
│   ├── favicon.ico
│   └── og-image.png
├── content/                    # ← Pipeline writes here
│   ├── posts/
│   │   └── 2026-03-01.md
│   └── resources.json
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout with nav, footer
│   │   ├── page.tsx            # Homepage — latest digest + archive list
│   │   ├── digest/
│   │   │   └── [slug]/
│   │   │       └── page.tsx    # Individual digest post page
│   │   ├── resources/
│   │   │   └── page.tsx        # Curated resources page
│   │   ├── about/
│   │   │   └── page.tsx        # About page explaining the project
│   │   └── api/
│   │       └── subscribe/
│   │           └── route.ts    # Email subscription endpoint (optional)
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── DigestCard.tsx      # Preview card for archive listing
│   │   ├── StoryCard.tsx       # Individual story within a digest
│   │   ├── ResourceCard.tsx    # Resource item display
│   │   ├── SignificanceBadge.tsx# Visual indicator for story importance
│   │   ├── CategoryTag.tsx     # Category label component
│   │   ├── TableOfContents.tsx # Sticky sidebar TOC for digest posts
│   │   ├── SearchBar.tsx       # Search across past digests
│   │   └── Newsletter.tsx      # Email signup form
│   ├── lib/
│   │   ├── posts.ts            # Read and parse markdown posts
│   │   ├── resources.ts        # Read and parse resources.json
│   │   └── search.ts           # Client-side search logic
│   └── styles/
│       └── globals.css         # Tailwind base + custom styles
```

### Step-by-Step Build Instructions

#### Step 1: Project Setup

- Use Next.js 14+ with App Router
- TypeScript, Tailwind CSS
- Dependencies:
  ```
  next
  react
  tailwindcss
  gray-matter           # Parse YAML frontmatter
  react-markdown        # Render markdown content
  remark-gfm            # GitHub-flavored markdown support
  rehype-highlight      # Code syntax highlighting
  date-fns              # Date formatting
  ```
- Configure Tailwind with a clean, editorial design system:
  - Use `Inter` or `Geist` for body text
  - Use a monospace font for code/technical content
  - Dark/light mode support
  - Color palette: muted, professional, with accent color for significance indicators

#### Step 2: Content Parsing (`lib/posts.ts`)

```typescript
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export interface DigestPost {
  slug: string;              // "2026-03-01"
  title: string;
  date: string;
  weekNumber: number;
  year: number;
  summary: string;
  topStories: TopStory[];
  categories: string[];
  resources: Resource[];
  content: string;           // Raw markdown body
}

export interface TopStory {
  title: string;
  category: string;
  significance: number;
  sourceUrl: string;
}

export interface Resource {
  title: string;
  url: string;
  type: string;
  description: string;
}

export function getAllPosts(): DigestPost[] {
  // Read content/posts/*.md, parse frontmatter, sort by date descending
}

export function getPostBySlug(slug: string): DigestPost | null {
  // Read single post by filename
}
```

#### Step 3: Build Pages

**Homepage (`page.tsx`)**:
- Hero section: site name, tagline ("Your weekly deep-dive into AI & technology"), brief description
- Latest digest prominently featured with summary and top stories preview
- Archive section: list of past digests as cards with date, title, summary
- Clean and scannable — readers should immediately see the latest content

**Digest Post Page (`digest/[slug]/page.tsx`)**:
- Full rendered markdown content
- Sticky table of contents sidebar (desktop) generated from markdown headings
- Top stories metadata displayed at the top (categories, significance scores)
- "Resources from this week" section at the bottom
- Previous/Next digest navigation
- Reading time estimate
- Share buttons (Twitter/X, LinkedIn, copy link)

**Resources Page (`resources/page.tsx`)**:
- Parse `content/resources.json`
- Display resources grouped by category (newsletters, podcasts, YouTube, blogs, etc.)
- Each resource card shows: name, description, link, type badge
- This is a living page that accumulates resources over time
- Filter/search functionality

**About Page (`about/page.tsx`)**:
- Explain this is an autonomous AI-curated digest
- How it works (brief technical overview for curious readers)
- Data sources listed
- Transparency: mention Claude is used for analysis

#### Step 4: Components

**`DigestCard.tsx`**: Used on homepage for archive listing
- Date, title, summary
- Category tags shown as pills
- Top 3 stories listed
- Link to full digest

**`StoryCard.tsx`**: Used within a digest post for top stories section
- Story title, category tag, significance badge
- Link to source
- Brief one-line description

**`SignificanceBadge.tsx`**: Visual indicator
- 9-10: Red/critical indicator
- 7-8: Orange/important
- 4-6: Blue/notable
- Uses a simple colored dot or bar, not distracting

**`TableOfContents.tsx`**:
- Extract headings from rendered markdown
- Sticky on desktop, collapsible on mobile
- Highlight current section on scroll (Intersection Observer)

**`CategoryTag.tsx`**: Colored pill/chip for categories
- ai-research: purple
- ai-industry: blue
- tech: green
- open-source: orange
- policy: red

#### Step 5: Design Requirements

The design should feel like a premium newsletter/publication:

- **Typography**: Large, readable body text (18px+). Clear hierarchy with headings.
- **Whitespace**: Generous margins and padding. Content should breathe.
- **Color**: Minimal. Mostly black/white/gray with color reserved for category tags and significance indicators. Dark mode should be equally polished.
- **Layout**: Max content width ~720px for readability. Sidebar for TOC on wide screens.
- **Mobile**: Fully responsive. TOC becomes a floating button/drawer on mobile.
- **Performance**: Static generation (SSG) for all pages. No client-side data fetching. Should score 95+ on Lighthouse.
- **SEO**: Proper meta tags, Open Graph images, structured data (Article schema).

#### Step 6: Static Generation

- All pages should use `generateStaticParams` for static generation
- The site rebuilds when new content is pushed to the repo
- Configure `next.config.js` for static export if deploying to static hosting
- Or use Vercel for automatic rebuilds on git push

#### Step 7: RSS Feed

- Generate an RSS feed at `/feed.xml`
- Include title, date, summary, and link for each digest
- Use `next.config.js` rewrites or a route handler to serve XML

---

## INTEGRATION & DEPLOYMENT

After both agents complete their work:

### Repository Structure

```
ai-tech-digest/
├── pipeline/            # Agent 1's output
├── website/             # Agent 2's output
├── content/             # Shared directory
│   ├── posts/
│   └── resources.json
├── .github/
│   └── workflows/
│       ├── weekly-digest.yml    # Runs pipeline weekly
│       └── deploy.yml           # Deploys website on push
└── README.md
```

### GitHub Actions: Weekly Pipeline (`.github/workflows/weekly-digest.yml`)

```yaml
name: Weekly Digest Pipeline

on:
  schedule:
    - cron: '0 14 * * 0'  # Every Sunday at 2 PM UTC
  workflow_dispatch:        # Manual trigger for testing

jobs:
  generate-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install pipeline dependencies
        run: cd pipeline && pip install -e .

      - name: Run pipeline
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: cd pipeline && python -m src.main

      - name: Commit and push new digest
        run: |
          git config user.name "AI Digest Bot"
          git config user.email "bot@ai-digest.dev"
          git add content/
          git commit -m "digest: Week $(date +%V), $(date +%Y)"
          git push
```

### GitHub Actions: Deploy Website (`.github/workflows/deploy.yml`)

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
        run: |
          cd website
          npm ci
          npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./website
```

### Environment Secrets Required

Set these in GitHub repo settings → Secrets:
- `ANTHROPIC_API_KEY` — For Claude API calls in the pipeline
- `GITHUB_TOKEN` — Already available, for GitHub Trending scraping
- `VERCEL_TOKEN` — For deployment (if using Vercel)
- `VERCEL_ORG_ID` — Vercel organization ID
- `VERCEL_PROJECT_ID` — Vercel project ID
- `REDDIT_CLIENT_ID` — Optional, for Reddit API
- `REDDIT_CLIENT_SECRET` — Optional, for Reddit API

### Estimated Running Costs

- Claude API: ~$1-3 per weekly run (Sonnet for triage + Opus for deep analysis)
- Vercel hosting: Free tier is sufficient
- GitHub Actions: Free tier is sufficient
- Total: ~$5-15/month

---

## QUALITY CHECKLIST

Before considering the project complete, verify:

### Pipeline
- [ ] All collectors fetch data successfully
- [ ] Deduplication correctly groups same-story articles
- [ ] Claude analysis output matches the data contract format
- [ ] Generated markdown renders correctly
- [ ] Git publish creates clean commits
- [ ] Pipeline completes in under 10 minutes
- [ ] Error handling: pipeline doesn't crash if one source is down
- [ ] Logs are clear and useful for debugging

### Website
- [ ] Homepage displays latest digest correctly
- [ ] Individual digest pages render full markdown properly
- [ ] Table of contents generates from headings and tracks scroll
- [ ] Resources page displays grouped resources
- [ ] Dark mode works without flash
- [ ] Mobile responsive on all pages
- [ ] Lighthouse score 95+ (Performance, Accessibility, SEO)
- [ ] RSS feed validates
- [ ] Category tags and significance badges display correctly

### Integration
- [ ] Pipeline output is correctly consumed by the website
- [ ] GitHub Actions weekly cron fires and completes
- [ ] Website auto-deploys when new content is pushed
- [ ] Full end-to-end test: manual pipeline trigger → site updates
