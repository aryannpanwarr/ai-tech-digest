'use client';

import { useEffect, useState } from 'react';

interface TocItem {
  id: string;
  text: string;
  level: number;
}

function extractHeadings(content: string): TocItem[] {
  const headings: TocItem[] = [];
  const regex = /^(#{2,3})\s+(.+)$/gm;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const level = match[1].length;
    const text = match[2].trim();
    const id = text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-');
    headings.push({ id, text, level });
  }
  return headings;
}

export default function TableOfContents({ content }: { content: string }) {
  const [activeId, setActiveId] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const headings = extractHeadings(content);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        }
      },
      { rootMargin: '-80px 0px -80% 0px' }
    );

    headings.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [headings]);

  if (headings.length === 0) return null;

  const tocContent = (
    <nav className="space-y-1">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-3">
        On this page
      </h4>
      {headings.map((h) => (
        <a
          key={h.id}
          href={`#${h.id}`}
          onClick={() => setIsOpen(false)}
          className={`block text-sm py-1 transition-colors ${
            h.level === 3 ? 'pl-4' : ''
          } ${
            activeId === h.id
              ? 'text-blue-600 dark:text-blue-400 font-medium'
              : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
          }`}
        >
          {h.text}
        </a>
      ))}
    </nav>
  );

  return (
    <>
      {/* Desktop TOC - sticky sidebar */}
      <aside className="hidden lg:block w-[280px] shrink-0">
        <div className="sticky top-24 max-h-[calc(100vh-200px)] overflow-y-auto pr-4">
          {tocContent}
        </div>
      </aside>

      {/* Mobile TOC - floating button + drawer */}
      <div className="lg:hidden fixed bottom-6 right-6 z-40">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-12 h-12 rounded-full bg-blue-600 text-white shadow-lg flex items-center justify-center hover:bg-blue-700 transition-colors"
          aria-label="Table of contents"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
        </button>
      </div>

      {isOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/50" onClick={() => setIsOpen(false)} />
          <div className="absolute bottom-0 left-0 right-0 bg-white dark:bg-slate-900 rounded-t-2xl p-6 max-h-[60vh] overflow-y-auto">
            {tocContent}
          </div>
        </div>
      )}
    </>
  );
}
