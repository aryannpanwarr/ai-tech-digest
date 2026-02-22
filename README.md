# AI & Tech Weekly Digest

Autonomous weekly AI/tech editorial pipeline + static website.

Live deployment: **https://ai-tech-digest-flax.vercel.app**

## What This Project Does

Every week, the pipeline:

- Collects stories from multiple sources (RSS, Hacker News, Reddit, ArXiv, GitHub)
- Deduplicates and ranks them
- Uses Gemini models for triage, deep analysis, and resource curation
- Publishes markdown digest posts + `resources.json` into `content/`
- Commits updates and triggers website deploy

The website renders those generated files into an editorial-style digest experience.

## Project Structure

- `pipeline/` — Python pipeline (collectors, analysis, publishing)
- `website/` — Next.js frontend
- `content/` — generated markdown posts + shared resources data
- `.github/workflows/` — weekly pipeline and deploy automation

## Tech Stack

- Backend: Python 3.11+, `feedparser`, `httpx`, `crawl4ai`, `google-genai`
- Frontend: Next.js 14, TypeScript, Tailwind CSS
- Hosting/CI: GitHub Actions + Vercel

## Local Setup

### 1) Pipeline

```bash
cd pipeline
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
cp .env.example .env
```

Set at least:

- `GEMINI_API_KEY`

Optional but recommended:

- `GITHUB_TOKEN`
- `GEMINI_FLASH_MODEL` (default: `gemini-3-flash-preview`)
- `GEMINI_PRO_MODEL` (default: `gemini-3-pro-preview`)

Run tests:

```bash
.venv/bin/pytest -q
```

Run pipeline:

```bash
python -m src.main
```

### 2) Website

```bash
cd website
npm install
npm run dev
```

Build:

```bash
npm run build
```

## Automation

- Weekly digest generation: `.github/workflows/weekly-digest.yml`
- Website deploy: `.github/workflows/deploy.yml`

Required GitHub Actions secrets:

- `GEMINI_API_KEY`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## Data Contract

- Digest posts: `content/posts/*.md` with YAML frontmatter schema
- Resource index: `content/resources.json`

Both pipeline and website rely on this shared contract.

## Repository

GitHub: https://github.com/aryannpanwarr/ai-tech-digest
