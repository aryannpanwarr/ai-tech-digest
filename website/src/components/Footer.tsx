import Link from 'next/link';

export default function Footer() {
  const repoUrl = process.env.NEXT_PUBLIC_REPO_URL || 'https://github.com';

  return (
    <footer className="border-t border-[var(--border-color)] mt-16">
      <div className="max-w-with-toc mx-auto px-6 md:px-12 py-8 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-[var(--text-secondary)]">
        <div className="flex items-center gap-1">
          <span>Powered by Gemini AI</span>
          <span className="mx-1">&middot;</span>
          <Link href="/about" className="hover:text-[var(--text-primary)] transition-colors">
            About this project
          </Link>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/feed.xml" className="hover:text-[var(--text-primary)] transition-colors">
            RSS
          </Link>
          <a
            href={repoUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-[var(--text-primary)] transition-colors"
          >
            GitHub
          </a>
          <span>&copy; {new Date().getFullYear()}</span>
        </div>
      </div>
    </footer>
  );
}
