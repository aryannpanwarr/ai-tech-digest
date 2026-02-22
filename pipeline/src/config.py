"""Configuration, data models, and source lists for the pipeline."""

from pydantic import BaseModel, Field
from datetime import datetime


class RawArticle(BaseModel):
    title: str
    url: str
    source: str  # e.g. "hackernews", "arxiv", "rss:techcrunch"
    content: str  # Full text or substantial excerpt
    published_at: datetime | None = None
    score: int | None = None  # Upvotes, stars, etc.
    tags: list[str] = Field(default_factory=list)


# --- RSS Feeds ---
RSS_FEEDS = [
    ("techcrunch", "https://techcrunch.com/feed/"),
    ("theverge", "https://www.theverge.com/rss/index.xml"),
    ("arstechnica", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
    ("google-ai", "https://blog.google/technology/ai/rss/"),
    ("openai", "https://openai.com/blog/rss.xml"),
    ("anthropic", "https://www.anthropic.com/rss.xml"),
    ("huggingface", "https://huggingface.co/blog/feed.xml"),
    ("simonwillison", "https://simonwillison.net/atom/everything/"),
    ("lilianweng", "https://lilianweng.github.io/index.xml"),
    ("mlengineer", "https://newsletter.mlengineer.io/feed"),
]

# --- Reddit ---
SUBREDDITS = [
    "MachineLearning",
    "artificial",
    "LocalLLaMA",
    "technology",
    "programming",
]

# --- ArXiv ---
ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
ARXIV_MAX_RESULTS = 30

# --- AI/Tech keywords for filtering ---
AI_TECH_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "neural network", "llm", "large language model", "gpt", "gemini",
    "claude", "transformer", "diffusion", "generative", "nlp",
    "computer vision", "robotics", "autonomous", "openai", "anthropic",
    "google ai", "meta ai", "mistral", "llama", "open source",
    "gpu", "cuda", "pytorch", "tensorflow", "hugging face",
    "fine-tuning", "rlhf", "rag", "vector database", "embedding",
    "agent", "copilot", "automation", "semiconductor", "chip",
]

# --- Category values ---
VALID_CATEGORIES = ["ai-research", "ai-industry", "tech", "open-source", "policy"]

# --- Resource types ---
VALID_RESOURCE_TYPES = ["paper", "article", "tool", "repo", "video", "podcast", "newsletter"]

# --- HTTP settings ---
HTTP_TIMEOUT = 15.0
MAX_RETRIES = 2
USER_AGENT = "AI-Tech-Digest-Bot/1.0 (https://github.com/ai-tech-digest)"
