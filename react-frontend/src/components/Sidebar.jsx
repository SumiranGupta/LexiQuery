import { NavLink } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
  LayoutDashboard, Upload, Bot, History, Settings,
  Sun, Moon, Zap, ChevronLeft, ChevronRight,
} from 'lucide-react';
import { useState } from 'react';

const NAV = [
  { to: '/',          icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload',    icon: Upload,          label: 'Upload Center' },
  { to: '/assistant', icon: Bot,             label: 'AI Assistant' },
  { to: '/history',   icon: History,         label: 'Query History' },
  { to: '/system',    icon: Settings,        label: 'System Status' },
];

export default function Sidebar() {
  const { theme, toggle } = useTheme();
  const [collapsed, setCollapsed] = useState(false);
  const dark = theme === 'dark';

  return (
    <aside
      className={`relative flex flex-col h-screen transition-all duration-300 border-r
        ${collapsed ? 'w-[72px]' : 'w-64'}`}
      style={{
        background: dark ? 'rgba(12, 18, 34, 0.85)' : 'rgba(255,255,255,0.85)',
        borderColor: dark ? 'rgba(99,102,241,0.12)' : 'rgba(15,23,42,0.08)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
      }}
    >
      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(c => !c)}
        className={`
          absolute -right-3 top-7 z-10 flex items-center justify-center
          w-6 h-6 rounded-full border text-xs transition
          ${dark
            ? 'bg-slate-800 border-indigo-500/30 text-indigo-400 hover:bg-slate-700'
            : 'bg-white border-slate-300 text-slate-500 hover:bg-slate-50'}
        `}
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>

      {/* Brand */}
      <div className="flex items-center gap-2 px-5 py-6">
        <Zap className="text-indigo-500 shrink-0" size={24} />
        {!collapsed && (
          <div>
            <div className="text-lg font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              LexiQuery
            </div>
            <div className={`text-[10px] tracking-widest uppercase ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
              AI Knowledge Platform
            </div>
          </div>
        )}
      </div>

      <div className={`mx-4 border-t ${dark ? 'border-indigo-500/10' : 'border-slate-200'}`} />

      {/* Navigation label */}
      {!collapsed && (
        <div className={`px-5 pt-4 pb-2 text-[10px] uppercase tracking-widest font-medium
          ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
          Navigation
        </div>
      )}

      {/* Nav links */}
      <nav className="flex-1 px-3 space-y-1 mt-1">
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) => `
              flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all
              ${collapsed ? 'justify-center' : ''}
              ${isActive
                ? dark
                  ? 'bg-gradient-to-r from-indigo-600/30 to-purple-600/20 text-indigo-300 border border-indigo-500/20'
                  : 'bg-gradient-to-r from-indigo-50 to-purple-50 text-indigo-700 border border-indigo-200'
                : dark
                  ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }
            `}
          >
            <Icon size={18} />
            {!collapsed && label}
          </NavLink>
        ))}
      </nav>

      <div className={`mx-4 border-t ${dark ? 'border-indigo-500/10' : 'border-slate-200'}`} />

      {/* Tech Stack */}
      {!collapsed && (
        <div className="px-5 py-3">
          <div className={`text-[10px] uppercase tracking-widest font-medium mb-2
            ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
            Tech Stack
          </div>
          <div className={`text-xs space-y-1 ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
            <div>🧠 <span className={dark ? 'text-slate-300' : 'text-slate-700'}>Llama 3.3 70B</span></div>
            <div>🔗 <span className={dark ? 'text-slate-300' : 'text-slate-700'}>MiniLM-L6</span></div>
            <div>💾 <span className={dark ? 'text-slate-300' : 'text-slate-700'}>FAISS</span></div>
            <div>⚡ <span className={dark ? 'text-slate-300' : 'text-slate-700'}>Groq</span></div>
          </div>
        </div>
      )}

      <div className={`mx-4 border-t ${dark ? 'border-indigo-500/10' : 'border-slate-200'}`} />

      {/* Theme Toggle */}
      <div className="px-3 py-4">
        <button
          onClick={toggle}
          className={`
            flex items-center justify-center gap-2 w-full px-3 py-2 rounded-lg text-sm font-medium transition
            ${dark
              ? 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60'
              : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}
          `}
        >
          {dark ? <Sun size={16} /> : <Moon size={16} />}
          {!collapsed && (dark ? 'Light Mode' : 'Dark Mode')}
        </button>
        {!collapsed && (
          <div className={`text-center text-[10px] mt-1.5 ${dark ? 'text-slate-600' : 'text-slate-400'}`}>
            Currently: {dark ? '🌙 Dark' : '☀️ Light'}
          </div>
        )}
      </div>

      {/* Footer */}
      {!collapsed && (
        <div className={`px-5 pb-5 text-center`}>
          <div className="flex items-center justify-center gap-1.5 mb-0.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse-dot" />
            <span className={`text-[10px] font-medium ${dark ? 'text-emerald-500' : 'text-emerald-600'}`}>System Online</span>
          </div>
          <div className={`text-[10px] ${dark ? 'text-slate-600' : 'text-slate-400'}`}>
            LexiQuery v2.0 &nbsp;•&nbsp; Enterprise
          </div>
        </div>
      )}
    </aside>
  );
}
