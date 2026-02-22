const categoryStyles: Record<string, string> = {
  'ai-research': 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
  'ai-industry': 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
  'tech': 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300',
  'open-source': 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300',
  'policy': 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-300',
};

const categoryLabels: Record<string, string> = {
  'ai-research': 'AI Research',
  'ai-industry': 'AI Industry',
  'tech': 'Tech',
  'open-source': 'Open Source',
  'policy': 'Policy',
};

export default function CategoryTag({ category }: { category: string }) {
  const style = categoryStyles[category] || 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300';
  const label = categoryLabels[category] || category;

  return (
    <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-medium ${style}`}>
      {label}
    </span>
  );
}
