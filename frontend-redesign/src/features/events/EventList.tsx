import React, { useState, useMemo } from 'react';
import { Search, Sparkles, SlidersHorizontal } from 'lucide-react';
import { CampusEvent, EventCategory } from '../../types';
import { EventCard } from './EventCard';
import { EventDetailModal } from './EventDetailModal';
import { HeroBanner } from './HeroBanner';
import { Input } from '../../components/ui/Input';

interface EventListProps {
  events: CampusEvent[];
}

const CATEGORIES: ('All' | EventCategory)[] = [
  'All',
  'Technical',
  'Cultural',
  'Sports',
  'Workshop',
  'Seminar',
];

export const EventList: React.FC<EventListProps> = ({ events }) => {
  const [selectedCategory, setSelectedCategory] = useState<'All' | EventCategory>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeEvent, setActiveEvent] = useState<CampusEvent | null>(null);

  const filteredEvents = useMemo(() => {
    return events.filter((event) => {
      const matchesCategory =
        selectedCategory === 'All' || event.category === selectedCategory;
      const matchesSearch =
        searchQuery.trim() === '' ||
        event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        event.venue.toLowerCase().includes(searchQuery.toLowerCase()) ||
        event.description.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [events, selectedCategory, searchQuery]);

  const recommendedEvents = useMemo(() => {
    return events.filter((e) => e.isRecommended);
  }, [events]);

  return (
    <div className="space-y-8">
      {/* Hero Banner */}
      <HeroBanner />

      {/* Top Search & Filter Bar */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        {/* Category Pills Strip */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`rounded-full px-4 py-1.5 text-xs font-semibold transition-all duration-200 whitespace-nowrap ${
                selectedCategory === cat
                  ? 'bg-primary text-white shadow-glow'
                  : 'bg-surface hover:bg-elevated text-slate-300 border border-white/10'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Search Input with ⌘K styling */}
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search events, venues..."
            className="pl-10 pr-12 rounded-full"
          />
          <kbd className="absolute right-3.5 top-1/2 -translate-y-1/2 rounded border border-white/10 bg-slate-900 px-1.5 py-0.5 text-[10px] font-mono text-slate-400">
            ⌘K
          </kbd>
        </div>
      </div>

      {/* Recommended Feeds Strip (If active and not searching) */}
      {searchQuery === '' && selectedCategory === 'All' && recommendedEvents.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-amber-400" />
              <h2 className="text-lg font-bold text-white">Recommended For You</h2>
            </div>
            <span className="text-xs font-medium text-slate-400">
              Personalized based on club interests
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendedEvents.map((event) => (
              <EventCard key={`rec-${event.id}`} event={event} onSelect={setActiveEvent} />
            ))}
          </div>
        </section>
      )}

      {/* Main Catalogue Grid */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white">
            {selectedCategory === 'All' ? 'All Campus Events' : `${selectedCategory} Events`}
          </h2>
          <span className="text-xs text-slate-400">
            Showing {filteredEvents.length} listings
          </span>
        </div>

        {filteredEvents.length === 0 ? (
          <div className="rounded-2xl border border-white/10 bg-surface/50 p-12 text-center">
            <SlidersHorizontal className="mx-auto h-12 w-12 text-slate-500 mb-3" />
            <h3 className="text-lg font-bold text-white">No Events Found</h3>
            <p className="text-sm text-slate-400 mt-1">
              Try adjusting your keyword search or category filter.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEvents.map((event) => (
              <EventCard key={event.id} event={event} onSelect={setActiveEvent} />
            ))}
          </div>
        )}
      </section>

      {/* Detail Dialog */}
      <EventDetailModal event={activeEvent} onClose={() => setActiveEvent(null)} />
    </div>
  );
};
