import { notFound } from 'next/navigation';
import Link from 'next/link';
import type { Metadata } from 'next';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypeHighlight from 'rehype-highlight';
import { getAllPosts, getPostBySlug, getAdjacentPosts } from '@/lib/posts';
import StoryCard from '@/components/StoryCard';
import ResourceCard from '@/components/ResourceCard';
import CategoryTag from '@/components/CategoryTag';
import TableOfContents from '@/components/TableOfContents';
import ShareButtons from '@/components/ShareButtons';
import { formatDate } from '@/lib/utils';

export function generateStaticParams() {
  const posts = getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const post = getPostBySlug(params.slug);
  if (!post) return { title: 'Not Found' };

  return {
    title: post.title,
    description: post.summary,
    openGraph: {
      title: post.title,
      description: post.summary,
      type: 'article',
      publishedTime: post.date,
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.summary,
    },
  };
}

export default function DigestPage({ params }: { params: { slug: string } }) {
  const post = getPostBySlug(params.slug);
  if (!post) notFound();

  const { prev, next } = getAdjacentPosts(params.slug);
  const siteUrl = 'https://ai-tech-digest.dev';
  const postUrl = `${siteUrl}/digest/${post.slug}`;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    datePublished: post.date,
    description: post.summary,
    url: postUrl,
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="max-w-with-toc mx-auto px-6 md:px-12 py-8">
        {/* Header section */}
        <header className="max-w-content mb-8">
          <div className="text-sm text-[var(--text-secondary)] mb-3">
            {formatDate(post.date)} &middot; Week {post.weekNumber}, {post.year} &middot; {post.readingTime} min read
          </div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">{post.title}</h1>
          <p className="text-lg text-[var(--text-secondary)] mb-4">{post.summary}</p>
          <div className="flex flex-wrap gap-2 mb-6">
            {post.categories.map((cat) => (
              <CategoryTag key={cat} category={cat} />
            ))}
          </div>
        </header>

        {/* Top stories */}
        <section className="max-w-content mb-8 p-4 rounded-lg border border-[var(--border-color)]">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-3">
            Top Stories This Week
          </h2>
          {post.topStories.map((story, i) => (
            <StoryCard key={i} story={story} />
          ))}
        </section>

        {/* Main content + TOC */}
        <div className="flex gap-8">
          <article className="max-w-content min-w-0 flex-1 prose-custom">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeSlug, rehypeHighlight]}
            >
              {post.content}
            </ReactMarkdown>
          </article>
          <TableOfContents content={post.content} />
        </div>

        {/* Resources from this week */}
        {post.resources.length > 0 && (
          <section className="max-w-content mt-12">
            <h2 className="text-lg font-bold mb-4">Resources From This Week</h2>
            <div className="grid gap-3 md:grid-cols-2">
              {post.resources.map((r, i) => (
                <ResourceCard key={i} resource={r} />
              ))}
            </div>
          </section>
        )}

        {/* Share */}
        <div className="max-w-content mt-8 pt-6 border-t border-[var(--border-color)]">
          <ShareButtons title={post.title} url={postUrl} />
        </div>

        {/* Prev/Next navigation */}
        <nav className="max-w-content mt-8 pt-6 border-t border-[var(--border-color)] flex justify-between gap-4">
          {next ? (
            <Link
              href={`/digest/${next.slug}`}
              className="flex-1 p-4 rounded-lg border border-[var(--border-color)] hover:border-blue-300 dark:hover:border-blue-700 transition-colors"
            >
              <div className="text-xs text-[var(--text-secondary)] mb-1">&larr; Older</div>
              <div className="text-sm font-medium line-clamp-1">{next.title}</div>
            </Link>
          ) : <div />}
          {prev ? (
            <Link
              href={`/digest/${prev.slug}`}
              className="flex-1 p-4 rounded-lg border border-[var(--border-color)] hover:border-blue-300 dark:hover:border-blue-700 transition-colors text-right"
            >
              <div className="text-xs text-[var(--text-secondary)] mb-1">Newer &rarr;</div>
              <div className="text-sm font-medium line-clamp-1">{prev.title}</div>
            </Link>
          ) : <div />}
        </nav>
      </div>
    </>
  );
}
