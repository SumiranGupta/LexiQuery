import { useTheme } from '../context/ThemeContext';

export default function PageHeader({ icon, title, subtitle, badge }) {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  return (
    <div className="mb-7 animate-fade-in-up">
      <div className="flex items-center gap-3 mb-1">
        <div className={`flex items-center justify-center w-10 h-10 rounded-xl text-xl shrink-0
          ${dark ? 'bg-indigo-600/20 border border-indigo-500/20' : 'bg-indigo-50 border border-indigo-200'}`}>
          {icon}
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className={`text-2xl font-bold tracking-tight ${dark ? 'text-white' : 'text-slate-900'}`}>
              {title}
            </h1>
            {badge && (
              <span className="text-xs px-2 py-0.5 rounded-full font-semibold bg-indigo-600/20 text-indigo-400 border border-indigo-500/20">
                {badge}
              </span>
            )}
          </div>
          {subtitle && (
            <p className={`text-sm ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
              {subtitle}
            </p>
          )}
        </div>
      </div>
      <div className={`h-px mt-4 ${dark ? 'bg-gradient-to-r from-indigo-500/20 via-purple-500/10 to-transparent' : 'bg-gradient-to-r from-indigo-200/60 via-purple-100/40 to-transparent'}`} />
    </div>
  );
}
