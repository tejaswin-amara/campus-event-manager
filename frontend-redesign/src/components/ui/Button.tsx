import React from 'react';
import { cn } from '../../lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg' | 'icon';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    const variantStyles = {
      primary: 'bg-primary hover:bg-primary-hover text-white shadow-glow border border-primary/40',
      secondary: 'bg-surface hover:bg-elevated text-slate-200 border border-white/10',
      outline: 'bg-transparent hover:bg-white/5 text-slate-200 border border-white/20',
      ghost: 'bg-transparent hover:bg-white/10 text-slate-300 hover:text-white border-transparent',
      danger: 'bg-rose-600 hover:bg-rose-700 text-white shadow-lg border border-rose-500/40',
    };

    const sizeStyles = {
      sm: 'px-3 py-1.5 text-xs rounded-lg gap-1.5',
      md: 'px-4 py-2 text-sm rounded-xl gap-2',
      lg: 'px-6 py-3 text-base rounded-xl gap-2.5 font-semibold',
      icon: 'p-2 rounded-lg text-sm',
    };

    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center font-medium transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background',
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
