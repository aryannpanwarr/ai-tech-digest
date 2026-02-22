import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-jetbrains)', 'monospace'],
      },
      colors: {
        category: {
          'ai-research': { light: '#a855f7', dark: '#c084fc' },
          'ai-industry': { light: '#3b82f6', dark: '#60a5fa' },
          'tech': { light: '#10b981', dark: '#34d399' },
          'open-source': { light: '#f97316', dark: '#fb923c' },
          'policy': { light: '#f43f5e', dark: '#fb7185' },
        },
      },
      maxWidth: {
        'content': '720px',
        'with-toc': '1100px',
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '720px',
            fontSize: '18px',
            lineHeight: '1.7',
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};

export default config;
