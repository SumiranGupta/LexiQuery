/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',   // toggles via <html class="dark">
  safelist: ['dark', 'light'],  // prevent purging of theme classes
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
      },
      backgroundImage: {
        'gradient-dark': 'linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0f172a 100%)',
        'gradient-light': 'linear-gradient(135deg, #f0f4ff 0%, #e8ecf4 50%, #f8fafc 100%)',
      },
    },
  },
  plugins: [],
}
