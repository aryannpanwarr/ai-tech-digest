'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { formatDate } from '@/lib/utils';

interface SearchResult {
  slug: string;
  title: string;
  date: string;
  summary: string;
  storyHeadlines: string[];
}

export default function SearchBar({ posts }: { posts: SearchResult[] }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.trim().length < 2) {
        setResults([]);
        setIsOpen(false);
        return;
      }
      const q = query.toLowerCase();
      const matches = posts.filter(
        (p) => {
          const haystack = [
            p.title,
            p.summary,
            ...p.storyHeadlines,
          ].join(' ').toLowerCase();
          return haystack.includes(q);
        }
      );
      setResults(matches.slice(0, 5));
      setIsOpen(matches.length > 0);
    }, 300);
    return () => clearTimeout(timer);
  }, [query, posts]);

  return (
    <div ref={ref} className="relative w-full max-w-md">
      <div className="relative">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-secondary)]"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search past digests..."
          className="w-full pl-10 pr-4 py-2 text-sm rounded-lg border border-[var(--border-color)] bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500"
        />
      </div>
      {isOpen && results.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-white dark:bg-slate-900 border border-[var(--border-color)] rounded-lg shadow-lg overflow-hidden z-50">
          {results.map((r) => (
            <Link
              key={r.slug}
              href={`/digest/${r.slug}`}
              onClick={() => {
                setIsOpen(false);
                setQuery('');
              }}
              className="block px-4 py-3 hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors border-b border-[var(--border-color)] last:border-0"
            >
              <div className="text-sm font-medium line-clamp-1">{r.title}</div>
              <div className="text-xs text-[var(--text-secondary)] mt-0.5">{formatDate(r.date)}</div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
