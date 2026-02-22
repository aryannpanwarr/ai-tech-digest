import type { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: {
    default: 'AI & Tech Weekly Digest',
    template: '%s | AI & Tech Weekly Digest',
  },
  description: 'Your weekly deep-dive into AI & technology. Autonomously curated. Thoroughly analyzed. Every Sunday.',
  openGraph: {
    title: 'AI & Tech Weekly Digest',
    description: 'Your weekly deep-dive into AI & technology.',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI & Tech Weekly Digest',
    description: 'Your weekly deep-dive into AI & technology.',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var theme = localStorage.getItem('theme');
                  if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                    document.documentElement.classList.add('dark');
                  }
                } catch(e) {}
              })();
            `,
          }}
        />
      </head>
      <body className="font-sans antialiased min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
