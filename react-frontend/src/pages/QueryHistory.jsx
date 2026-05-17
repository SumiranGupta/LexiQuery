import { useTheme } from '../context/ThemeContext';
import { usePolling } from '../hooks/usePolling';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import PageHeader from '../components/PageHeader';
import { Clock, Zap, Package, ChevronDown, ChevronRight } from 'lucide-react';
import { useState } from 'react';

export default function QueryHistory() {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  const { data: queries } = usePolling(() => api.getQueries(50), 5000);
  const [expanded, setExpanded] = useState({});

  const toggle = (id) => setExpanded(p => ({ ...p, [id]: !p[id] }));

  if (!queries) return null;

  const total = queries.length;
  const avgLatency = total > 0
    ? (queries.reduce((s, q) => s + (q.total_latency_ms || 0), 0) / total).toFixed(0)
    : 0;
  const avgChunks = total > 0
    ? (queries.reduce((s, q) => s + (q.chunks_retrieved || 0), 0) / total).toFixed(1)
    : 0;

  return (
    <div>
      <PageHeader icon="📋" title="Query History" subtitle="Browse your past queries and AI responses" />

      {queries.length === 0 ? (
        <div className="glass-card text-center py-16">
          <span className="text-4xl">🔍</span>
          <p className={`mt-4 text-lg font-medium ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
            No queries yet
          </p>
          <p className={`text-sm mt-1 ${dark ? 'text-slate-600' : 'text-slate-400'}`}>
            Head to the AI Assistant to start asking questions
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-3 gap-4 mb-6">
            <MetricCard icon="💬" value={total} label="Total Queries" />
            <MetricCard icon="⚡" value={`${avgLatency}ms`} label="Avg Latency" />
            <MetricCard icon="📦" value={avgChunks} label="Avg Chunks" />
          </div>

          <div className="space-y-2">
            {queries.map((q, i) => {
              const isOpen = expanded[i];
              const label = q.query_text?.length > 100
                ? q.query_text.slice(0, 100) + '...'
                : q.query_text;

              return (
                <div key={i} className="glass-card !p-0 overflow-hidden">
                  <button
                    onClick={() => toggle(i)}
                    className={`w-full flex items-center gap-3 px-4 py-3 text-left transition
                      ${dark ? 'hover:bg-slate-800/40' : 'hover:bg-slate-50'}`}
                  >
                    {isOpen ? <ChevronDown size={16} className="text-indigo-500 shrink-0" />
                      : <ChevronRight size={16} className={`shrink-0 ${dark ? 'text-slate-500' : 'text-slate-400'}`} />}
                    <span className={`flex-1 text-sm font-medium truncate
                      ${dark ? 'text-slate-200' : 'text-slate-700'}`}>
                      🔹 {label}
                    </span>
                    <div className={`flex items-center gap-3 text-xs shrink-0
                      ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                      <span className="flex items-center gap-1"><Clock size={12} />{q.created_at?.slice(0, 16)}</span>
                      <span className="flex items-center gap-1"><Zap size={12} />{q.total_latency_ms?.toFixed(0)}ms</span>
                      <span className="flex items-center gap-1"><Package size={12} />{q.chunks_retrieved}</span>
                    </div>
                  </button>

                  {isOpen && (
                    <div className={`px-4 pb-4 pt-1 border-t
                      ${dark ? 'border-slate-700/50' : 'border-slate-200'}`}>
                      <div className="mb-3">
                        <div className={`text-xs font-semibold mb-1 ${dark ? 'text-indigo-400' : 'text-indigo-600'}`}>
                          Question
                        </div>
                        <div className={`text-sm ${dark ? 'text-slate-300' : 'text-slate-600'}`}>
                          {q.query_text}
                        </div>
                      </div>
                      {q.response_preview && (
                        <div>
                          <div className={`text-xs font-semibold mb-1 ${dark ? 'text-purple-400' : 'text-purple-600'}`}>
                            Response
                          </div>
                          <div className={`text-sm ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
                            {q.response_preview}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
