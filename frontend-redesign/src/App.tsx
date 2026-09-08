import React, { useState } from 'react';
import { Layout } from './components/Layout';
import { EventList } from './features/events/EventList';
import { KpiGrid } from './features/admin/KpiGrid';
import { EventTable } from './features/admin/EventTable';
import { MOCK_EVENTS } from './data/mockEvents';
import { CampusEvent } from './types';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<'student' | 'admin'>('student');
  const [events, setEvents] = useState<CampusEvent[]>(MOCK_EVENTS);

  const handleDeleteEvent = (id: number) => {
    setEvents((prev) => prev.filter((e) => e.id !== id));
  };

  const handleCreateEvent = (newEventData: Omit<CampusEvent, 'id' | 'registeredCount'>) => {
    const newEvent: CampusEvent = {
      ...newEventData,
      id: Math.max(...events.map((e) => e.id), 0) + 1,
      registeredCount: 0,
    };
    setEvents((prev) => [newEvent, ...prev]);
  };

  return (
    <Layout currentView={currentView} onViewChange={setCurrentView}>
      {currentView === 'student' ? (
        <EventList events={events} />
      ) : (
        <div className="space-y-8">
          <div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Control Plane & Analytics
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Real-time monitoring, event publishing, capacity enforcement, and student engagement telemetry
            </p>
          </div>

          <KpiGrid events={events} />

          <EventTable
            events={events}
            onDelete={handleDeleteEvent}
            onCreate={handleCreateEvent}
          />
        </div>
      )}
    </Layout>
  );
};

export default App;
