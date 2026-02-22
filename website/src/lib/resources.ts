import fs from 'fs';
import path from 'path';

const RESOURCES_PATH = path.join(process.cwd(), '..', 'content', 'resources.json');

export interface ResourceEntry {
  name: string;
  url: string;
  description: string;
  frequency?: string;
}

export interface ResourceIndex {
  last_updated: string;
  categories: Record<string, ResourceEntry[]>;
}

export function getResources(): ResourceIndex {
  try {
    if (!fs.existsSync(RESOURCES_PATH)) {
      return { last_updated: '', categories: {} };
    }
    const raw = fs.readFileSync(RESOURCES_PATH, 'utf8');
    return JSON.parse(raw) as ResourceIndex;
  } catch {
    return { last_updated: '', categories: {} };
  }
}
