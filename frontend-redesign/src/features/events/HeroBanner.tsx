import React from 'react';
import { Calendar, Sparkles, ArrowRight } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const HeroBanner: React.FC = () => {
  return (
    <section className="relative overflow-hidden rounded-3xl border border-primary/30 bg-gradient-to-br from-primary/15 via-purple-950/20 to-background p-6 sm:p-8 lg:p-10 shadow-2xl">
      {/* Decorative gradient blur */}
      <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-primary/20 blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-2xl space-y-4">
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/40 bg-primary/20 px-3 py-1 text-xs font-semibold text-primary-light">
          <Sparkles className="h-3.5 w-3.5" />
          <span>CAMPUS CALENDAR FALL 2026</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white lg:text-5xl">
          Discover & Connect with Campus Life
        </h1>

        <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
          From cutting-edge multi-agent hackathons to varsity championships and cultural galas,
          find your community and amplify your university journey.
        </p>

        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Button variant="primary" size="md">
            <Calendar className="h-4 w-4" />
            <span>Explore Events</span>
          </Button>
          <Button variant="outline" size="md">
            <span>Learn More</span>
            <ArrowRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </section>
  );
};
