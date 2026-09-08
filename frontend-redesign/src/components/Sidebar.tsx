import React from 'react';
import { Calendar, LayoutDashboard, Shield, Sparkles } from 'lucide-react';

interface SidebarProps {
  currentView: 'student' | 'admin';
  onViewChange: (view: 'student' | 'admin') => void;
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentView,
  onViewChange,
  isOpen,
  onClose,
}) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 flex w-64 flex-col border-r border-white/10 bg-surface/95 backdrop-blur-xl p-6 transition-transform duration-300 lg:static lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand */}
        <div className="flex items-center gap-3 pb-6 border-b border-white/10">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-primary to-indigo-400 text-white font-black text-lg shadow-glow">
            CC
          </div>
          <div>
            <h1 className="font-extrabold text-white tracking-tight leading-tight">CampusConnect</h1>
            <div className="flex items-center gap-1.5 text-[11px] text-emerald-400 font-medium">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>System Live</span>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="mt-6 flex-1 space-y-2">
          <button
            onClick={() => {
              onViewChange('student');
              onClose();
            }}
            className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition-all ${
              currentView === 'student'
                ? 'bg-primary text-white shadow-glow'
                : 'text-slate-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            <Calendar className="h-4 w-4" />
            <span>Discover Events</span>
          </button>

          <button
            onClick={() => {
              onViewChange('admin');
              onClose();
            }}
            className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition-all ${
              currentView === 'admin'
                ? 'bg-primary text-white shadow-glow'
                : 'text-slate-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            <LayoutDashboard className="h-4 w-4" />
            <span>Admin Console</span>
          </button>
        </nav>

        {/* Bottom User Card */}
        <div className="rounded-2xl border border-white/10 bg-card/60 p-4">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary-light font-bold text-sm">
              {currentView === 'admin' ? 'A' : 'S'}
            </div>
            <div className="overflow-hidden">
              <p className="text-xs font-bold text-white truncate">
                {currentView === 'admin' ? 'Administrator' : 'Student Member'}
              </p>
              <p className="text-[10px] text-slate-400 flex items-center gap-1">
                {currentView === 'admin' ? <Shield className="h-3 w-3 text-rose-400" /> : <Sparkles className="h-3 w-3 text-amber-400" />}
                {currentView === 'admin' ? 'Admin Role' : 'Active Account'}
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
