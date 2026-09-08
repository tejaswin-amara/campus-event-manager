import React, { useState } from 'react';
import { Search, Plus, Trash2, Edit3, Download } from 'lucide-react';
import { CampusEvent } from '../../types';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { formatDate } from '../../lib/utils';
import { CreateEventModal } from './CreateEventModal';

interface EventTableProps {
  events: CampusEvent[];
  onDelete: (id: number) => void;
  onCreate: (event: Omit<CampusEvent, 'id' | 'registeredCount'>) => void;
}

export const EventTable: React.FC<EventTableProps> = ({ events, onDelete, onCreate }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  const filtered = events.filter((e) =>
    e.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.venue.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const exportCsv = () => {
    const headers = ['ID', 'Title', 'Category', 'Venue', 'DateTime', 'Capacity', 'Registrations'];
    const rows = events.map((e) => [
      e.id,
      `"${e.title.replace(/"/g, '""')}"`,
      e.category,
      `"${e.venue.replace(/"/g, '""')}"`,
      e.dateTime,
      e.maxCapacity ?? 'Unlimited',
      e.registeredCount,
    ]);

    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `campus-events-${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="rounded-2xl border border-white/10 bg-card/80 backdrop-blur-md overflow-hidden">
      {/* Table Header Bar */}
      <div className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between border-b border-white/10">
        <div>
          <h3 className="text-base font-bold text-white">Event Registry & Lifecycle</h3>
          <p className="text-xs text-slate-400">Manage listings, check capacity limits, and download CSV</p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="relative w-full sm:w-60">
            <Search className="absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400" />
            <Input
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search registry..."
              className="h-9 pl-9 text-xs rounded-lg"
            />
          </div>

          <Button variant="outline" size="sm" onClick={exportCsv}>
            <Download className="h-3.5 w-3.5" />
            <span>Export CSV</span>
          </Button>

          <Button variant="primary" size="sm" onClick={() => setIsCreateOpen(true)}>
            <Plus className="h-3.5 w-3.5" />
            <span>New Event</span>
          </Button>
        </div>
      </div>

      {/* Table Body */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-surface/60 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            <tr>
              <th className="px-6 py-3.5">Event Title</th>
              <th className="px-6 py-3.5">Category</th>
              <th className="px-6 py-3.5">Schedule</th>
              <th className="px-6 py-3.5">Venue</th>
              <th className="px-6 py-3.5">Capacity</th>
              <th className="px-6 py-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {filtered.map((event) => (
              <tr key={event.id} className="hover:bg-white/[0.02] transition-colors">
                <td className="px-6 py-4 font-semibold text-white">
                  <div className="flex items-center gap-3">
                    <div className="h-9 w-9 rounded-lg bg-surface border border-white/10 overflow-hidden flex-shrink-0">
                      {event.imageUrl ? (
                        <img src={event.imageUrl} alt="" className="h-full w-full object-cover" />
                      ) : (
                        <div className="h-full w-full bg-slate-800 flex items-center justify-center text-xs text-slate-500">
                          CC
                        </div>
                      )}
                    </div>
                    <div>
                      <div className="font-bold text-white line-clamp-1">{event.title}</div>
                      <div className="text-xs text-slate-400 line-clamp-1">ID: #{event.id}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <Badge variant={event.category}>{event.category}</Badge>
                </td>
                <td className="px-6 py-4 text-xs text-slate-300 whitespace-nowrap">
                  {formatDate(event.dateTime)}
                </td>
                <td className="px-6 py-4 text-xs text-slate-300">{event.venue}</td>
                <td className="px-6 py-4 text-xs">
                  <span className="font-bold text-white">{event.registeredCount}</span>
                  <span className="text-slate-500"> / {event.maxCapacity ?? '∞'}</span>
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="inline-flex items-center gap-2">
                    <button
                      className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
                      title="Edit Event"
                      aria-label="Edit Event"
                    >
                      <Edit3 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => onDelete(event.id)}
                      className="p-1.5 text-slate-400 hover:text-rose-400 rounded-lg hover:bg-rose-500/10 transition-colors"
                      title="Delete Event"
                      aria-label="Delete Event"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-10 text-center text-slate-500 text-sm">
                  No matching events found in registry.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <CreateEventModal
        open={isCreateOpen}
        onClose={() => setIsCreateOpen(false)}
        onCreate={onCreate}
      />
    </div>
  );
};
