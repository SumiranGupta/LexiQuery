import { useTheme } from '../context/ThemeContext';
import { usePolling } from '../hooks/usePolling';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import PageHeader from '../components/PageHeader';
import {
  ResponsiveContainer, AreaChart, Area, BarChart, Bar,
  PieChart, Pie, Cell, XAxis, YAxis, Tooltip, CartesianGrid,
} from 'recharts';

const PIE_COLORS = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#818cf8', '#4f46e5'];

export default function Dashboard() {
  const { theme } = useTheme();
  const dark = theme === 'dark';
  const textMuted = dark ? '#94a3b8' : '#64748b';
  const gridColor = dark ? 'rgba(99,102,241,0.1)' : 'rgba(0,0,0,0.06)';

  const { data: stats } = usePolling(api.getStats, 4000);
  const { data: queries } = usePolling(() => api.getQueries(50), 5000);
  const { data: documents } = usePolling(api.getDocuments, 5000);
  const { data: topSources } = usePolling(api.getTopSources, 5000);

  // Build timeline data
  const timelineData = (() => {
    if (!queries?.length) return [];
    const counts = {};
    queries.forEach(q => {
      const d = (q.created_at || '').slice(0, 10);
      if (d) counts[d] = (counts[d] || 0) + 1;
    });
    return Object.entries(counts).map(([date, count]) => ({ date, count }));
  })();

  // Build latency data
  const latencyData = (queries || []).slice(0, 20).map((q, i) => ({
    idx: i + 1,
    latency: q.retrieval_latency_ms || 0,
  }));

  // Build pie data
  const pieData = (() => {
    if (!documents?.length) return [];
    const ext = {};
    documents.forEach(d => {
      const name = d.filename || '';
      const e = name.includes('.') ? name.split('.').pop().toUpperCase() : 'OTHER';
      ext[e] = (ext[e] || 0) + 1;
    });
    return Object.entries(ext).map(([name, value]) => ({ name, value }));
  })();

  return (
    <div className="animate-fade-in-up">
      <PageHeader icon="📊" title="Dashboard" subtitle="Platform overview and real-time analytics" />

      {/* Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <MetricCard icon="📄" value={stats?.total_documents ?? '—'} label="Documents" />
        <MetricCard icon="🧩" value={stats?.total_chunks ?? '—'} label="Chunks" />
        <MetricCard icon="💬" value={stats?.total_queries ?? '—'} label="Queries" />
        <MetricCard icon="⚡" value={stats ? `${stats.avg_retrieval_latency_ms}ms` : '—'} label="Avg Latency" />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
        {/* Query Timeline */}
        <div className="glass-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className={`text-sm font-semibold ${dark ? 'text-white' : 'text-slate-800'}`}>Query Activity</h3>
              <p className={`text-xs mt-0.5 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>Queries over time</p>
            </div>
            {timelineData.length > 0 && (
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium border
                ${dark ? 'bg-indigo-600/15 text-indigo-400 border-indigo-500/20' : 'bg-indigo-50 text-indigo-600 border-indigo-200'}`}>
                {timelineData.reduce((s, d) => s + d.count, 0)} total
              </span>
            )}
          </div>
          {timelineData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={timelineData}>
                <defs>
                  <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                <XAxis dataKey="date" tick={{ fill: textMuted, fontSize: 11 }} />
                <YAxis tick={{ fill: textMuted, fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    background: dark ? '#1e293b' : '#fff',
                    border: `1px solid ${dark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: 8, fontSize: 12,
                    color: dark ? '#f1f5f9' : '#0f172a',
                  }}
                />
                <Area type="monotone" dataKey="count" stroke="#6366f1" strokeWidth={2}
                  fill="url(#areaGrad)" dot={{ r: 4, fill: '#8b5cf6' }} />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <p className={`text-sm ${dark ? 'text-slate-500' : 'text-slate-400'} text-center py-12`}>
              No query data yet — start asking questions!
            </p>
          )}
        </div>

        {/* Latency Chart */}
        <div className="glass-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className={`text-sm font-semibold ${dark ? 'text-white' : 'text-slate-800'}`}>Retrieval Latency</h3>
              <p className={`text-xs mt-0.5 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>Last 20 queries (ms)</p>
            </div>
            {stats && (
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium border
                ${dark ? 'bg-emerald-600/15 text-emerald-400 border-emerald-500/20' : 'bg-emerald-50 text-emerald-600 border-emerald-200'}`}>
                avg {stats.avg_retrieval_latency_ms}ms
              </span>
            )}
          </div>
          {latencyData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={latencyData}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                <XAxis dataKey="idx" tick={{ fill: textMuted, fontSize: 11 }} />
                <YAxis tick={{ fill: textMuted, fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    background: dark ? '#1e293b' : '#fff',
                    border: `1px solid ${dark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: 8, fontSize: 12,
                    color: dark ? '#f1f5f9' : '#0f172a',
                  }}
                />
                <Bar dataKey="latency" radius={[4, 4, 0, 0]}>
                  {latencyData.map((_, i) => (
                    <Cell key={i} fill={i % 2 === 0 ? '#6366f1' : '#8b5cf6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className={`text-sm ${dark ? 'text-slate-500' : 'text-slate-400'} text-center py-12`}>
              No latency data yet.
            </p>
          )}
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Document Distribution */}
        <div className="glass-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className={`text-sm font-semibold ${dark ? 'text-white' : 'text-slate-800'}`}>Document Types</h3>
              <p className={`text-xs mt-0.5 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>Distribution by format</p>
            </div>
          </div>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={90}
                  paddingAngle={3} dataKey="value" label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  labelLine={{ stroke: textMuted }}
                >
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: dark ? '#1e293b' : '#fff',
                    border: `1px solid ${dark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: 8, fontSize: 12,
                    color: dark ? '#f1f5f9' : '#0f172a',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className={`text-sm ${dark ? 'text-slate-500' : 'text-slate-400'} text-center py-12`}>
              No documents uploaded yet.
            </p>
          )}
        </div>

        {/* Top Documents */}
        <div className="glass-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className={`text-sm font-semibold ${dark ? 'text-white' : 'text-slate-800'}`}>Top Documents</h3>
              <p className={`text-xs mt-0.5 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>By chunk count</p>
            </div>
          </div>
          {topSources?.length > 0 ? (
            <div className="space-y-2">
              {topSources.map((doc, i) => (
                <div key={i} className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition
                  ${dark ? 'bg-slate-800/40 hover:bg-slate-800/70' : 'bg-slate-50 hover:bg-slate-100'}`}>
                  <span className={`w-6 h-6 flex items-center justify-center rounded-lg text-xs font-bold shrink-0
                    ${i === 0 ? 'bg-amber-500/20 text-amber-400' : i === 1 ? 'bg-slate-400/20 text-slate-400' : i === 2 ? 'bg-orange-500/20 text-orange-400' : dark ? 'bg-slate-700 text-slate-500' : 'bg-slate-200 text-slate-500'}`}>
                    {i + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className={`text-sm font-medium truncate ${dark ? 'text-slate-200' : 'text-slate-700'}`}>
                      {doc.filename}
                    </div>
                    <div className={`text-xs ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                      {doc.page_count} pages
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-0.5 rounded-full shrink-0
                    ${dark ? 'bg-indigo-600/20 text-indigo-400' : 'bg-indigo-100 text-indigo-600'}`}>
                    {doc.chunk_count} chunks
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className={`text-sm ${dark ? 'text-slate-500' : 'text-slate-400'} text-center py-12`}>
              No documents indexed yet.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
