"""All LLM prompt templates for the analysis pipeline."""

TRIAGE_PROMPT = """You are an expert AI and technology analyst. You will receive a JSON array
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
}"""

ANALYSIS_PROMPT = """You are writing the weekly AI & Tech Digest. You will receive the triaged
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
[Cross-cutting analysis: what these stories mean together, emerging trends]"""

RESOURCES_PROMPT = """Given the articles and analysis from this week, recommend 5-10 high-quality
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
}"""
