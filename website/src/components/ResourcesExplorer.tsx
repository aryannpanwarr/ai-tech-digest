'use client';

import { useMemo, useState } from 'react';
import type { ResourceEntry } from '@/lib/resources';

const categoryLabels: Record<string, string> = {
  newsletters: 'Newsletters',
  podcasts: 'Podcasts',
  youtube_channels: 'YouTube Channels',
  blogs: 'Blogs',
  research_trackers: 'Research Trackers',
  tools: 'Tools',
  communities: 'Communities',
};

interface ResourcesExplorerProps {
  categories: Record<string, ResourceEntry[]>;
}

export default function ResourcesExplorer({ categories }: ResourcesExplorerProps) {
  const [query, setQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');

  const categoryOptions = useMemo(
    () => Object.keys(categories).filter((key) => (categories[key] || []).length > 0),
    [categories]
  );

  const filtered = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    const matchesQuery = (item: ResourceEntry) => {
      if (!normalizedQuery) {
        return true;
      }

      return [item.name, item.description, item.url]
        .join(' ')
        .toLowerCase()
        .includes(normalizedQuery);
    };

    return Object.entries(categories)
      .filter(([key]) => activeCategory === 'all' || key === activeCategory)
      .map(([key, items]) => [key, items.filter(matchesQuery)] as const)
      .filter(([, items]) => items.length > 0);
  }, [activeCategory, categories, query]);

  return (
    <div>
      <div className="mb-8 grid gap-3 md:grid-cols-[1fr_220px]">
        <label className="block">
          <span className="sr-only">Search resources</span>
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search resources..."
            className="w-full rounded-lg border border-[var(--border-color)] bg-transparent px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30"
          />
        </label>

        <label className="block">
          <span className="sr-only">Filter by category</span>
          <select
            value={activeCategory}
            onChange={(event) => setActiveCategory(event.target.value)}
            className="w-full rounded-lg border border-[var(--border-color)] bg-transparent px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30"
          >
            <option value="all">All categories</option>
            {categoryOptions.map((key) => (
              <option key={key} value={key}>
                {categoryLabels[key] || key}
              </option>
            ))}
          </select>
        </label>
      </div>

      {filtered.length === 0 ? (
        <div className="rounded-lg border border-[var(--border-color)] p-8 text-center">
          <p className="text-[var(--text-secondary)]">No resources matched your filters.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map(([key, items]) => (
            <details key={key} className="rounded-lg border border-[var(--border-color)] p-4" open>
              <summary className="cursor-pointer list-none text-lg font-semibold">
                {categoryLabels[key] || key}
                <span className="ml-2 text-sm font-normal text-[var(--text-secondary)]">
                  ({items.length})
                </span>
              </summary>

              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {items.map((item, index) => (
                  <div key={`${item.url}-${index}`} className="rounded-lg border border-[var(--border-color)] p-4">
                    <div className="mb-1 flex items-start justify-between gap-3">
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm font-medium transition-colors hover:text-blue-600 dark:hover:text-blue-400"
                      >
                        {item.name}
                      </a>
                      {item.frequency ? (
                        <span className="shrink-0 rounded-full border border-[var(--border-color)] px-2 py-0.5 text-xs text-[var(--text-secondary)]">
                          {item.frequency}
                        </span>
                      ) : null}
                    </div>
                    <p className="text-sm text-[var(--text-secondary)]">{item.description}</p>
                  </div>
                ))}
              </div>
            </details>
          ))}
        </div>
      )}
    </div>
  );
}
