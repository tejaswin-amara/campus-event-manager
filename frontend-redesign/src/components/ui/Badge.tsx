import React from 'react';
import { cn } from '../../lib/utils';
import { EventCategory } from '../../types';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'outline' | 'secondary' | 'success' | 'warning' | 'info' | 'destructive' | EventCategory;
}

export const Badge: React.FC<BadgeProps> = ({ className, variant = 'default', children, ...props }) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'Technical':
        return 'bg-category-technical/15 text-indigo-300 border-category-technical/30';
      case 'Cultural':
        return 'bg-category-cultural/15 text-pink-300 border-category-cultural/30';
      case 'Sports':
        return 'bg-category-sports/15 text-emerald-300 border-category-sports/30';
      case 'Workshop':
        return 'bg-category-workshop/15 text-amber-300 border-category-workshop/30';
      case 'Seminar':
        return 'bg-category-seminar/15 text-cyan-300 border-category-seminar/30';
      case 'success':
        return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
      case 'warning':
        return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
      case 'info':
        return 'bg-sky-500/15 text-sky-400 border-sky-500/30';
      case 'destructive':
        return 'bg-rose-500/15 text-rose-400 border-rose-500/30';
      case 'secondary':
        return 'bg-secondary text-slate-300 border-white/10';
      case 'outline':
        return 'bg-transparent text-slate-200 border-white/20';
      default:
        return 'bg-primary/20 text-primary-light border-primary/30';
    }
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border transition-all',
        getVariantStyles(),
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
