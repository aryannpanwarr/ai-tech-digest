import Link from 'next/link';
import type { DigestPost } from '@/lib/posts';
import CategoryTag from './CategoryTag';
import { formatDate } from '@/lib/utils';

export default function DigestCard({ post }: { post: DigestPost }) {
  return (
    <Link
      href={`/digest/${post.slug}`}
      className="block p-5 rounded-lg border border-[var(--border-color)] hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-sm transition-all"
    >
      <div className="text-xs text-[var(--text-secondary)] mb-2">
        {formatDate(post.date)} &middot; Week {post.weekNumber} &middot; {post.readingTime} min read
      </div>
      <h3 className="font-semibold mb-2 line-clamp-2">{post.title}</h3>
      <p className="text-sm text-[var(--text-secondary)] line-clamp-2 mb-3">{post.summary}</p>
      <div className="flex flex-wrap gap-1.5">
        {post.categories.slice(0, 3).map((cat) => (
          <CategoryTag key={cat} category={cat} />
        ))}
      </div>
    </Link>
  );
}
