/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#09090b',
        foreground: '#f8fafc',
        card: {
          DEFAULT: '#181824',
          foreground: '#f8fafc',
          hover: '#222232',
        },
        surface: '#121218',
        elevated: '#262638',
        primary: {
          DEFAULT: '#6366f1',
          foreground: '#ffffff',
          hover: '#4f46e5',
          light: '#818cf8',
        },
        secondary: {
          DEFAULT: '#262638',
          foreground: '#f1f5f9',
        },
        muted: {
          DEFAULT: '#262638',
          foreground: '#94a3b8',
        },
        accent: {
          DEFAULT: '#f97316',
          foreground: '#ffffff',
          hover: '#ea580c',
        },
        category: {
          technical: '#6366f1',
          cultural: '#ec4899',
          sports: '#10b981',
          workshop: '#f59e0b',
          seminar: '#06b6d4',
        }
      },
      borderRadius: {
        lg: '16px',
        md: '10px',
        sm: '6px',
      },
      boxShadow: {
        glow: '0 0 24px -4px rgba(99, 102, 241, 0.25)',
      }
    },
  },
  plugins: [],
}
