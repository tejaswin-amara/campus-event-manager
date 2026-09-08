import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { Sidebar } from './Sidebar';

interface LayoutProps {
  currentView: 'student' | 'admin';
  onViewChange: (view: 'student' | 'admin') => void;
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ currentView, onViewChange, children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      {/* Sidebar Navigation */}
      <Sidebar
        currentView={currentView}
        onViewChange={onViewChange}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile Header */}
        <header className="flex h-16 items-center justify-between border-b border-white/10 bg-surface/80 px-4 backdrop-blur-md lg:hidden sticky top-0 z-30">
          <button
            onClick={() => setSidebarOpen(true)}
            className="rounded-lg p-2 text-slate-300 hover:bg-white/10"
            aria-label="Open sidebar"
          >
            <Menu className="h-6 w-6" />
          </button>
          <span className="font-extrabold text-white tracking-tight">CampusConnect</span>
          <span className="rounded-full bg-primary/20 px-2.5 py-0.5 text-xs font-semibold text-primary-light border border-primary/30">
            {currentView === 'admin' ? 'Admin' : 'Student'}
          </span>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-10 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
};
