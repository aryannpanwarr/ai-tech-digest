import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const POSTS_DIR = path.join(process.cwd(), '..', 'content', 'posts');

export interface TopStory {
  title: string;
  category: 'ai-research' | 'ai-industry' | 'tech' | 'open-source' | 'policy';
  significance: number;
  source_url: string;
}

export interface Resource {
  title: string;
  url: string;
  type: 'paper' | 'article' | 'tool' | 'repo' | 'video' | 'podcast' | 'newsletter';
  description: string;
}

export interface DigestPost {
  slug: string;
  title: string;
  date: string;
  weekNumber: number;
  year: number;
  summary: string;
  topStories: TopStory[];
  categories: string[];
  resources: Resource[];
  content: string;
  readingTime: number;
}

function calculateReadingTime(content: string): number {
  return Math.ceil(content.split(/\s+/).length / 200);
}

function parsePost(filename: string): DigestPost | null {
  const filePath = path.join(POSTS_DIR, filename);
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const { data, content } = matter(fileContents);

    const slug = filename.replace(/\.md$/, '');

    return {
      slug,
      title: data.title || '',
      date: data.date || '',
      weekNumber: data.week_number || 0,
      year: data.year || 0,
      summary: data.summary || '',
      topStories: (data.top_stories || []).map((s: any) => ({
        title: s.title || '',
        category: s.category || 'tech',
        significance: s.significance || 5,
        source_url: s.source_url || '',
      })),
      categories: data.categories || [],
      resources: (data.resources || []).map((r: any) => ({
        title: r.title || '',
        url: r.url || '',
        type: r.type || 'article',
        description: r.description || '',
      })),
      content,
      readingTime: calculateReadingTime(content),
    };
  } catch {
    return null;
  }
}

export function getAllPosts(): DigestPost[] {
  try {
    if (!fs.existsSync(POSTS_DIR)) {
      return [];
    }
    const filenames = fs.readdirSync(POSTS_DIR).filter((f) => f.endsWith('.md'));
    const posts = filenames
      .map(parsePost)
      .filter((p): p is DigestPost => p !== null);

    // Sort by date descending (newest first)
    posts.sort((a, b) => b.date.localeCompare(a.date));
    return posts;
  } catch {
    return [];
  }
}

export function getPostBySlug(slug: string): DigestPost | null {
  const filename = `${slug}.md`;
  return parsePost(filename);
}

export function getAdjacentPosts(slug: string): { prev: DigestPost | null; next: DigestPost | null } {
  const posts = getAllPosts();
  const index = posts.findIndex((p) => p.slug === slug);
  if (index === -1) return { prev: null, next: null };
  return {
    prev: index > 0 ? posts[index - 1] : null,
    next: index < posts.length - 1 ? posts[index + 1] : null,
  };
}
