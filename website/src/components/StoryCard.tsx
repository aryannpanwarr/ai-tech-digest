import type { TopStory } from '@/lib/posts';
import SignificanceBadge from './SignificanceBadge';
import CategoryTag from './CategoryTag';

export default function StoryCard({ story }: { story: TopStory }) {
  return (
    <div className="flex items-start gap-3 py-3 border-b border-[var(--border-color)] last:border-0">
      <SignificanceBadge score={story.significance} />
      <div className="flex-1 min-w-0">
        <a
          href={story.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium hover:text-blue-600 dark:hover:text-blue-400 transition-colors line-clamp-2"
        >
          {story.title}
          <svg className="inline-block w-3 h-3 ml-1 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
      <CategoryTag category={story.category} />
    </div>
  );
}
