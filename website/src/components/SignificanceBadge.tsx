function getConfig(score: number): { color: string; label: string } {
  if (score >= 9) return { color: 'bg-red-500 text-white', label: 'Critical' };
  if (score >= 7) return { color: 'bg-orange-500 text-white', label: 'Major' };
  if (score >= 4) return { color: 'bg-blue-500 text-white', label: 'Notable' };
  return { color: 'bg-gray-400 text-white', label: 'Minor' };
}

export default function SignificanceBadge({ score }: { score: number }) {
  const { color, label } = getConfig(score);

  return (
    <span className="inline-flex items-center gap-1.5" title={`Significance: ${score}/10 (${label})`}>
      <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${color}`}>
        {score}
      </span>
      <span className="text-xs text-[var(--text-secondary)] hidden sm:inline">{label}</span>
    </span>
  );
}
