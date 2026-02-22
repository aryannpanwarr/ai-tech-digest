import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About',
  description: 'About AI & Tech Weekly Digest — an autonomous AI-powered weekly digest.',
};

export default function AboutPage() {
  const repoUrl = process.env.NEXT_PUBLIC_REPO_URL || 'https://github.com';

  return (
    <div className="max-w-content mx-auto px-6 md:px-12 py-12">
      <h1 className="text-3xl font-bold tracking-tight mb-6">About This Project</h1>

      <div className="prose-custom">
        <h2>What is this?</h2>
        <p>
          AI & Tech Weekly Digest is an <strong>autonomous, AI-powered weekly digest</strong> of the most important
          developments in artificial intelligence and technology. Every Sunday, our pipeline collects, analyzes,
          and publishes a comprehensive digest — no human editors required.
        </p>

        <h2>How it works</h2>
        <p>The digest is produced through a fully automated pipeline:</p>
        <ol>
          <li>
            <strong>Collection</strong> — We scrape high-quality sources including RSS feeds from major tech publications,
            HackerNews top stories, Reddit AI communities, ArXiv papers, and trending GitHub repositories.
          </li>
          <li>
            <strong>Deduplication</strong> — Articles covering the same story are merged using URL normalization
            and fuzzy title matching.
          </li>
          <li>
            <strong>AI Analysis</strong> — Google&apos;s Gemini AI models triage the top stories, write deep analysis
            with context and connections, and curate the best resources for further reading.
          </li>
          <li>
            <strong>Publication</strong> — The digest is automatically committed to our repository, triggering
            a build and deploy of this website.
          </li>
        </ol>

        <h2>Data Sources</h2>
        <p>We collect from the following sources every week:</p>
        <ul>
          <li>TechCrunch, The Verge, Ars Technica</li>
          <li>Google AI Blog, OpenAI Blog, Anthropic Blog</li>
          <li>Hugging Face Blog, Simon Willison, Lilian Weng</li>
          <li>HackerNews (top and best stories)</li>
          <li>Reddit: r/MachineLearning, r/artificial, r/LocalLLaMA, r/technology, r/programming</li>
          <li>ArXiv (cs.AI, cs.LG, cs.CL, cs.CV categories)</li>
          <li>GitHub trending repositories (AI/ML topics)</li>
        </ul>

        <h2>Transparency</h2>
        <p>
          All analysis in this digest is generated using <strong>Google&apos;s Gemini AI models</strong>.
          Specifically, we currently use Gemini 3 Flash Preview for triage and resource curation,
          and Gemini 3 Pro Preview for the in-depth analysis writing. We believe in being transparent
          about AI-generated content.
        </p>

        <h2>Open Source</h2>
        <p>
          This entire project is open source. The pipeline code, website, and all generated content
          are available on{' '}
          <a href={repoUrl} target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
          . Contributions, feedback, and suggestions are welcome.
        </p>
      </div>
    </div>
  );
}
