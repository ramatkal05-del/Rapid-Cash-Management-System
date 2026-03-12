/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#07080e',
          surface1: '#0d0e18',
          surface2: '#131421',
          surface3: '#1a1b2e',
          border: '#252640',
        },
        accent: {
          primary: '#4f8ef7',
          secondary: '#6b8cff',
          purple: '#8b5cf6',
          success: '#10b981',
          danger: '#ef4444',
          warning: '#f59e0b',
        },
        text: {
          main: '#e8eaf6',
          muted: '#64748b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
