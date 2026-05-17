import { useTheme } from '../context/ThemeContext';
import { usePolling } from '../hooks/usePolling';
import { api } from '../api/client';
import PageHeader from '../components/PageHeader';
import {
  CheckCircle2, AlertTriangle, RotateCcw, RefreshCw,
  Trash2, Loader2,
} from 'lucide-react';
import { useState } from 'react';

export default function SystemStatus() {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  const { data: health, refresh } = usePolling(api.getHealth, 8000);
  const [resetting, setResetting] = useState(false);

  const handleReset = async () => {
    if (!confirm('This will delete all vectors and document records. Continue?')) return;
    setResetting(true);
    try {
      await api.resetSystem();
      refresh();
    } finally {
      setResetting(false);
    }
  };

  if (!health) return null;

  return (
    <div className="animate-fade-in-up">
      <PageHeader icon="⚙️" title="System Status" subtitle="Platform health and configuration" />

      {/* Health Checks */}
      <h3 className={`text-base font-semibold mb-3 ${dark ? 'text-white' : 'text-slate-800'}`}>
        🏥 Health Checks
      </h3>
      <div className="space-y-2 mb-6">
        {health.checks.map((c, i) => (
          <div key={i} className={`glass-card !py-3 !px-5 flex items-center justify-between`}>
            <div className="flex items-center gap-3">
              {c.healthy
                ? <CheckCircle2 size={18} className="text-emerald-500" />
                : <AlertTriangle size={18} className="text-amber-500" />}
              <div>
                <div className={`text-sm font-medium ${dark ? 'text-slate-200' : 'text-slate-700'}`}>
                  {c.name}
                </div>
                <div className={`text-xs ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                  {c.detail}
                </div>
              </div>
            </div>
            <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium
              ${c.healthy
                ? dark ? 'bg-emerald-900/40 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
                : dark ? 'bg-amber-900/40 text-amber-400' : 'bg-amber-100 text-amber-700'
              }`}>
              {c.healthy ? 'Healthy' : 'Warning'}
            </span>
          </div>
        ))}
      </div>

      {/* Config + System Info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <div className="glass-card">
          <h4 className={`text-sm font-semibold mb-3 ${dark ? 'text-white' : 'text-slate-800'}`}>
            🧠 AI Configuration
          </h4>
          <div className={`text-sm space-y-1.5 ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
            {Object.entries(health.config).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="capitalize">{k.replace(/_/g, ' ')}</span>
                <span className={`font-medium ${dark ? 'text-slate-200' : 'text-slate-700'}`}>{String(v)}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card">
          <h4 className={`text-sm font-semibold mb-3 ${dark ? 'text-white' : 'text-slate-800'}`}>
            💻 System Information
          </h4>
          <div className={`text-sm space-y-1.5 ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
            {Object.entries(health.system).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="capitalize">{k.replace(/_/g, ' ')}</span>
                <span className={`font-medium ${dark ? 'text-slate-200' : 'text-slate-700'}`}>{String(v)}</span>
              </div>
            ))}
            <div className="flex justify-between">
              <span>Vectors</span>
              <span className={`font-medium ${dark ? 'text-slate-200' : 'text-slate-700'}`}>
                {health.vectors}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <h3 className={`text-base font-semibold mb-3 ${dark ? 'text-white' : 'text-slate-800'}`}>
        🔧 Actions
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <button
          onClick={handleReset}
          disabled={resetting}
          className={`flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition
            ${dark
              ? 'bg-red-900/30 text-red-400 hover:bg-red-900/50 border border-red-500/20'
              : 'bg-red-50 text-red-600 hover:bg-red-100 border border-red-200'}`}
        >
          {resetting ? <Loader2 size={16} className="animate-spin" /> : <Trash2 size={16} />}
          Reset Vector Store
        </button>

        <button
          onClick={refresh}
          className={`flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition
            ${dark
              ? 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60 border border-slate-700/50'
              : 'bg-slate-100 text-slate-600 hover:bg-slate-200 border border-slate-200'}`}
        >
          <RefreshCw size={16} />
          Refresh Stats
        </button>

        <button
          onClick={async () => { await api.resetQueries(); refresh(); }}
          className={`flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition
            ${dark
              ? 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60 border border-slate-700/50'
              : 'bg-slate-100 text-slate-600 hover:bg-slate-200 border border-slate-200'}`}
        >
          <RotateCcw size={16} />
          Clear Query History
        </button>
      </div>
    </div>
  );
}
