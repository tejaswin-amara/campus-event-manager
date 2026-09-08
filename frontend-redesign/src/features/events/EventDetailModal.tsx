import React from 'react';
import { Calendar, MapPin, Users, ExternalLink, CalendarPlus } from 'lucide-react';
import { CampusEvent } from '../../types';
import { Dialog } from '../../components/ui/Dialog';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { formatDate } from '../../lib/utils';

interface EventDetailModalProps {
  event: CampusEvent | null;
  onClose: () => void;
}

export const EventDetailModal: React.FC<EventDetailModalProps> = ({ event, onClose }) => {
  if (!event) return null;

  const handleDownloadICS = () => {
    const icsData = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//CampusConnect//Event Manager//EN',
      'BEGIN:VEVENT',
      `SUMMARY:${event.title}`,
      `DESCRIPTION:${event.description.replace(/\n/g, ' ')}`,
      `LOCATION:${event.venue}`,
      `DTSTART:${new Date(event.dateTime).toISOString().replace(/[-:]/g, '').split('.')[0]}Z`,
      'STATUS:CONFIRMED',
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\r\n');

    const blob = new Blob([icsData], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${event.title.replace(/\s+/g, '_')}.ics`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Dialog open={Boolean(event)} onClose={onClose} className="max-w-3xl p-0 overflow-hidden">
      {/* Banner */}
      <div className="relative h-64 w-full bg-slate-900">
        {event.imageUrl ? (
          <img
            src={event.imageUrl}
            alt={event.title}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-slate-600">
            <Calendar className="h-16 w-16" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-surface via-surface/40 to-transparent" />
        <div className="absolute left-6 bottom-4 flex items-center gap-2">
          <Badge variant={event.category}>{event.category}</Badge>
          {event.isRecommended && <Badge variant="warning">★ Top Recommendation</Badge>}
        </div>
      </div>

      {/* Body Details */}
      <div className="p-6 sm:p-8 space-y-6">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            {event.title}
          </h2>
        </div>

        {/* Metadata Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 rounded-xl border border-white/10 bg-card/60 p-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary/20 p-2 text-primary-light">
              <Calendar className="h-5 w-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Schedule</p>
              <p className="text-sm font-semibold text-white">{formatDate(event.dateTime)}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-accent/20 p-2 text-accent">
              <MapPin className="h-5 w-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Venue</p>
              <p className="text-sm font-semibold text-white truncate">{event.venue}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-emerald-500/20 p-2 text-emerald-400">
              <Users className="h-5 w-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Capacity</p>
              <p className="text-sm font-semibold text-white">
                {event.maxCapacity ? `${event.registeredCount} / ${event.maxCapacity}` : 'Unlimited'}
              </p>
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">About this Event</h3>
          <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
            {event.description}
          </p>
        </div>

        {/* Recommendation Reasons */}
        {event.recommendationReasons && event.recommendationReasons.length > 0 && (
          <div className="space-y-2 rounded-xl border border-primary/20 bg-primary/10 p-4">
            <p className="text-xs font-bold uppercase tracking-wider text-primary-light">Why Recommended</p>
            <ul className="flex flex-wrap gap-2 pt-1">
              {event.recommendationReasons.map((reason, idx) => (
                <li key={idx} className="text-xs text-slate-200 bg-surface/80 px-2.5 py-1 rounded-md border border-white/10">
                  ✓ {reason}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-end gap-3 pt-4 border-t border-white/10">
          <Button variant="secondary" onClick={handleDownloadICS}>
            <CalendarPlus className="h-4 w-4" />
            <span>Add to Calendar (.ics)</span>
          </Button>

          {event.registrationLink && (
            <a
              href={event.registrationLink}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex"
            >
              <Button variant="primary">
                <span>Register External</span>
                <ExternalLink className="h-4 w-4" />
              </Button>
            </a>
          )}
        </div>
      </div>
    </Dialog>
  );
};
