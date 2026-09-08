import React from 'react';
import { Calendar, MapPin, Users, ArrowRight } from 'lucide-react';
import { CampusEvent } from '../../types';
import { Badge } from '../../components/ui/Badge';
import { formatDate } from '../../lib/utils';

interface EventCardProps {
  event: CampusEvent;
  onSelect: (event: CampusEvent) => void;
}

export const EventCard: React.FC<EventCardProps> = ({ event, onSelect }) => {
  const isFull = event.maxCapacity ? event.registeredCount >= event.maxCapacity : false;
  const capacityPercent = event.maxCapacity
    ? Math.min(100, Math.round((event.registeredCount / event.maxCapacity) * 100))
    : null;

  return (
    <article
      onClick={() => onSelect(event)}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onSelect(event);
        }
      }}
      tabIndex={0}
      role="button"
      aria-label={`View details for ${event.title}`}
      className="group relative flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-card/80 backdrop-blur-sm transition-all duration-300 hover:-translate-y-1.5 hover:border-primary/50 hover:shadow-glow focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
    >
      {/* Banner Media */}
      <div className="relative h-48 w-full overflow-hidden bg-surface">
        {event.imageUrl ? (
          <img
            src={event.imageUrl}
            alt={event.title}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-slate-900 text-slate-600">
            <Calendar className="h-12 w-12" />
          </div>
        )}

        {/* Floating Category Pill */}
        <div className="absolute left-3 top-3">
          <Badge variant={event.category}>{event.category}</Badge>
        </div>

        {/* Floating Recommendation / Status */}
        {event.isRecommended && (
          <div className="absolute right-3 top-3">
            <Badge variant="warning" className="shadow-lg">
              ★ Recommended
            </Badge>
          </div>
        )}
      </div>

      {/* Content Container */}
      <div className="flex flex-1 flex-col p-5">
        <h3 className="line-clamp-2 text-base font-bold text-white transition-colors group-hover:text-primary-light">
          {event.title}
        </h3>

        <div className="mt-3 space-y-2 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <Calendar className="h-3.5 w-3.5 text-primary" />
            <span className="text-slate-200 font-medium">{formatDate(event.dateTime)}</span>
          </div>

          <div className="flex items-center gap-2">
            <MapPin className="h-3.5 w-3.5 text-accent" />
            <span className="truncate">{event.venue}</span>
          </div>

          {event.maxCapacity && (
            <div className="flex items-center gap-2">
              <Users className="h-3.5 w-3.5 text-slate-400" />
              <span>
                {event.registeredCount} / {event.maxCapacity} seats ({capacityPercent}%)
              </span>
            </div>
          )}
        </div>

        {/* Capacity Progress Bar */}
        {capacityPercent !== null && (
          <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
            <div
              className={`h-full transition-all duration-500 ${
                capacityPercent >= 90
                  ? 'bg-rose-500'
                  : capacityPercent >= 70
                  ? 'bg-amber-500'
                  : 'bg-emerald-500'
              }`}
              style={{ width: `${capacityPercent}%` }}
            />
          </div>
        )}

        {/* Action Button Strip */}
        <div className="mt-auto pt-4 flex items-center justify-between border-t border-white/5">
          <span className="text-xs font-semibold text-primary-light group-hover:text-white flex items-center gap-1">
            View Details
            <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
          </span>
          {isFull ? (
            <span className="text-[11px] font-bold text-rose-400">Waitlist</span>
          ) : (
            <span className="text-[11px] font-medium text-emerald-400">Open</span>
          )}
        </div>
      </div>
    </article>
  );
};
