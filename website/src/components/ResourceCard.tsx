import type { Resource } from '@/lib/posts';

const typeBadgeStyles: Record<string, string> = {
  paper: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
  article: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
  tool: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300',
  repo: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300',
  video: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
  podcast: 'bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-300',
  newsletter: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300',
};

export default function ResourceCard({ resource }: { resource: Resource }) {
  const badgeStyle = typeBadgeStyles[resource.type] || typeBadgeStyles.article;

  return (
    <div className="p-4 rounded-lg border border-[var(--border-color)]">
      <div className="flex items-start gap-2 mb-2">
        <a
          href={resource.url}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium text-sm hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          {resource.title}
          <svg className="inline-block w-3 h-3 ml-1 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
        <span className={`shrink-0 px-2 py-0.5 rounded-full text-xs font-medium ${badgeStyle}`}>
          {resource.type}
        </span>
      </div>
      <p className="text-sm text-[var(--text-secondary)]">{resource.description}</p>
    </div>
  );
}
