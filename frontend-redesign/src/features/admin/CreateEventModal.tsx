import React, { useState } from 'react';
import { Dialog } from '../../components/ui/Dialog';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { CampusEvent, EventCategory } from '../../types';

interface CreateEventModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (event: Omit<CampusEvent, 'id' | 'registeredCount'>) => void;
}

export const CreateEventModal: React.FC<CreateEventModalProps> = ({ open, onClose, onCreate }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState<EventCategory>('Technical');
  const [venue, setVenue] = useState('');
  const [dateTime, setDateTime] = useState('');
  const [maxCapacity, setMaxCapacity] = useState('');
  const [registrationLink, setRegistrationLink] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate({
      title,
      category,
      venue,
      dateTime: dateTime || new Date().toISOString(),
      maxCapacity: maxCapacity ? parseInt(maxCapacity, 10) : undefined,
      registrationLink: registrationLink || undefined,
      description,
    });
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} title="Create New Event" className="max-w-xl">
      <form onSubmit={handleSubmit} className="space-y-4 pt-2">
        <div>
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Event Title *
          </label>
          <Input
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. AI Systems Architecture Hackathon"
            className="mt-1"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Category *
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value as EventCategory)}
              className="mt-1 flex h-10 w-full rounded-xl border border-white/10 bg-surface/80 px-3 py-2 text-sm text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
            >
              <option value="Technical">Technical</option>
              <option value="Cultural">Cultural</option>
              <option value="Sports">Sports</option>
              <option value="Workshop">Workshop</option>
              <option value="Seminar">Seminar</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Venue *
            </label>
            <Input
              required
              value={venue}
              onChange={(e) => setVenue(e.target.value)}
              placeholder="e.g. Innovation Hall"
              className="mt-1"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Date & Time *
            </label>
            <Input
              type="datetime-local"
              required
              value={dateTime}
              onChange={(e) => setDateTime(e.target.value)}
              className="mt-1 text-slate-200"
            />
          </div>

          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Max Capacity
            </label>
            <Input
              type="number"
              min="1"
              value={maxCapacity}
              onChange={(e) => setMaxCapacity(e.target.value)}
              placeholder="e.g. 150 (optional)"
              className="mt-1"
            />
          </div>
        </div>

        <div>
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Registration URL
          </label>
          <Input
            type="url"
            value={registrationLink}
            onChange={(e) => setRegistrationLink(e.target.value)}
            placeholder="https://forms.gle/..."
            className="mt-1"
          />
        </div>

        <div>
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Description *
          </label>
          <textarea
            required
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Key highlights, speaker bios, agenda..."
            className="mt-1 w-full rounded-xl border border-white/10 bg-surface/80 p-3 text-sm text-white placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
          />
        </div>

        <div className="flex items-center justify-end gap-3 pt-4 border-t border-white/10">
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant="primary">
            Publish Event
          </Button>
        </div>
      </form>
    </Dialog>
  );
};
