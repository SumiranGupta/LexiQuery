import { useTheme } from '../context/ThemeContext';

export default function MetricCard({ icon, value, label }) {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  return (
    <div className="glass-card metric-accent relative overflow-hidden text-center group">
      {/* Subtle background glow */}
      <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500
        ${dark ? 'bg-gradient-to-br from-indigo-600/5 to-purple-600/5' : 'bg-gradient-to-br from-indigo-50/80 to-purple-50/50'}`} />
      <div className="relative">
        <div className={`inline-flex items-center justify-center w-10 h-10 rounded-xl text-xl mb-3 mx-auto
          ${dark ? 'bg-slate-800/80 border border-slate-700/50' : 'bg-slate-100 border border-slate-200'}`}>
          {icon}
        </div>
        <div className="text-2xl font-bold tracking-tight text-gradient">
          {value}
        </div>
        <div className={`text-xs mt-1 font-medium uppercase tracking-wider
          ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
          {label}
        </div>
      </div>
    </div>
  );
}
