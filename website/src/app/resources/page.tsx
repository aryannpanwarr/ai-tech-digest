import type { Metadata } from 'next';
import { getResources } from '@/lib/resources';
import { formatDate } from '@/lib/utils';
import ResourcesExplorer from '@/components/ResourcesExplorer';

export const metadata: Metadata = {
  title: 'Resources',
  description: 'Curated AI and technology resources — newsletters, podcasts, blogs, tools, and communities.',
};

export default function ResourcesPage() {
  const data = getResources();
  const categories = Object.entries(data.categories).filter(
    ([, items]) => items.length > 0
  );

  return (
    <div className="max-w-content mx-auto px-6 md:px-12 py-12">
      <h1 className="text-3xl font-bold tracking-tight mb-2">Resources</h1>
      <p className="text-[var(--text-secondary)] mb-1">
        Curated tools, publications, and communities for staying up to date with AI & tech.
      </p>
      {data.last_updated && (
        <p className="text-sm text-[var(--text-secondary)] mb-8">
          Last updated: {formatDate(data.last_updated)}
        </p>
      )}

      {categories.length === 0 ? (
        <div className="p-8 rounded-lg border border-[var(--border-color)] text-center">
          <p className="text-[var(--text-secondary)]">No resources yet — check back soon!</p>
        </div>
      ) : (
        <ResourcesExplorer categories={data.categories} />
      )}
    </div>
  );
}
