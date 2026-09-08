export type EventCategory = 'Technical' | 'Cultural' | 'Sports' | 'Workshop' | 'Seminar';

export type EventStatus = 'Upcoming' | 'Ongoing' | 'Past';

export interface CampusEvent {
  id: number;
  title: string;
  description: string;
  category: EventCategory;
  venue: string;
  dateTime: string;
  endDateTime?: string;
  maxCapacity?: number;
  registeredCount: number;
  registrationLink?: string;
  imageUrl?: string;
  isRecommended?: boolean;
  recommendationReasons?: string[];
}

export interface KpiMetric {
  label: string;
  value: number | string;
  change?: string;
  subtitle: string;
  status: 'primary' | 'success' | 'info' | 'warning';
}
