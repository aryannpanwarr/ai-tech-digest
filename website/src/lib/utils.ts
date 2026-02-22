import { format, parseISO } from 'date-fns';

export function calculateReadingTime(content: string): number {
  return Math.ceil(content.split(/\s+/).length / 200);
}

export function formatDate(dateStr: string): string {
  try {
    return format(parseISO(dateStr), 'MMMM d, yyyy');
  } catch {
    return dateStr;
  }
}
