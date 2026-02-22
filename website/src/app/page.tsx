import Link from 'next/link';
import { getAllPosts } from '@/lib/posts';
import DigestCard from '@/components/DigestCard';
import StoryCard from '@/components/StoryCard';
import SearchBar from '@/components/SearchBar';
import { formatDate } from '@/lib/utils';

export default function HomePage() {
  const posts = getAllPosts();
  const latest = posts[0];
  const archive = posts.slice(1);

  if (!latest) {
    return (
      <div className="max-w-content mx-auto px-6 md:px-12 py-16 text-center">
        <h1 className="text-4xl font-bold tracking-tight mb-4">AI & Tech Weekly Digest</h1>
        <p className="text-lg text-[var(--text-secondary)] mb-2">Your weekly deep-dive into AI & technology</p>
        <p className="text-sm text-[var(--text-secondary)]">Autonomously curated. Thoroughly analyzed. Every Sunday.</p>
        <div className="mt-12 p-8 rounded-lg border border-[var(--border-color)]">
          <p className="text-[var(--text-secondary)]">No digests yet — check back Sunday!</p>
        </div>
      </div>
    );
  }

  const searchData = posts.map((p) => ({
    slug: p.slug,
    title: p.title,
    date: p.date,
    summary: p.summary,
    storyHeadlines: p.topStories.map((story) => story.title),
  }));

  return (
    <div className="max-w-with-toc mx-auto px-6 md:px-12">
      {/* Hero */}
      <section className="py-12 md:py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">AI & Tech Weekly Digest</h1>
        <p className="text-lg text-[var(--text-secondary)] mb-1">Your weekly deep-dive into AI & technology</p>
        <p className="text-sm text-[var(--text-secondary)]">Autonomously curated. Thoroughly analyzed. Every Sunday.</p>
      </section>

      {/* Search */}
      <section className="mb-12 flex justify-center">
        <SearchBar posts={searchData} />
      </section>

      {/* Latest Digest */}
      <section className="mb-16">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-6">Latest Digest</h2>
        <div className="p-6 md:p-8 rounded-xl border border-[var(--border-color)]">
          <div className="text-sm text-[var(--text-secondary)] mb-2">
            {formatDate(latest.date)} &middot; Week {latest.weekNumber} &middot; {latest.readingTime} min read
          </div>
          <h3 className="text-2xl font-bold mb-3">{latest.title}</h3>
          <p className="text-[var(--text-secondary)] mb-6">{latest.summary}</p>

          {/* Top stories preview */}
          <div className="mb-6">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-3">Top Stories</h4>
            <div className="space-y-0">
              {latest.topStories.slice(0, 3).map((story, i) => (
                <StoryCard key={i} story={story} />
              ))}
            </div>
          </div>

          <Link
            href={`/digest/${latest.slug}`}
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-sm"
          >
            Read this week&apos;s digest
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        </div>
      </section>

      {/* Archive */}
      {archive.length > 0 && (
        <section className="mb-16">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-6">Past Digests</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {archive.map((post) => (
              <DigestCard key={post.slug} post={post} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
