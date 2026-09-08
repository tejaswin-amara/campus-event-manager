import React from 'react';
import { Calendar, Users, TrendingUp, Cpu } from 'lucide-react';
import { CampusEvent } from '../../types';

interface KpiGridProps {
  events: CampusEvent[];
}

export const KpiGrid: React.FC<KpiGridProps> = ({ events }) => {
  const totalEvents = events.length;
  const totalRegistrations = events.reduce((acc, e) => acc + e.registeredCount, 0);
  const technicalCount = events.filter((e) => e.category === 'Technical').length;

  const kpis = [
    {
      label: 'TOTAL EVENTS',
      value: totalEvents,
      subtitle: 'Catalogued listings',
      icon: Calendar,
      color: 'text-primary',
      bg: 'bg-primary/10 border-primary/20',
    },
    {
      label: 'STUDENT INTEREST',
      value: totalRegistrations,
      subtitle: 'Total sign-ups recorded',
      icon: Users,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10 border-emerald-500/20',
    },
    {
      label: 'TECHNICAL PIPELINE',
      value: technicalCount,
      subtitle: 'Hackathons & workshops',
      icon: Cpu,
      color: 'text-indigo-400',
      bg: 'bg-indigo-500/10 border-indigo-500/20',
    },
    {
      label: 'AVERAGE CAPACITY',
      value: `${Math.round((totalRegistrations / Math.max(1, totalEvents)))} / event`,
      subtitle: 'Healthy attendance density',
      icon: TrendingUp,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {kpis.map((kpi, idx) => {
        const Icon = kpi.icon;
        return (
          <div
            key={idx}
            className="flex flex-col justify-between rounded-2xl border border-white/10 bg-card/80 p-5 backdrop-blur-md transition-all duration-300 hover:border-white/20 hover:shadow-lg"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold tracking-wider text-slate-400 uppercase">
                {kpi.label}
              </span>
              <div className={`rounded-xl border p-2 ${kpi.bg}`}>
                <Icon className={`h-4 w-4 ${kpi.color}`} />
              </div>
            </div>
            <div className="mt-4">
              <div className="text-3xl font-extrabold text-white tracking-tight">
                {kpi.value}
              </div>
              <p className="text-xs text-slate-400 mt-1">{kpi.subtitle}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};
