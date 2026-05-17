import { useState, useCallback } from 'react';
import { useTheme } from '../context/ThemeContext';
import { usePolling } from '../hooks/usePolling';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import PageHeader from '../components/PageHeader';
import { Upload, FileText, Loader2, CheckCircle2, AlertCircle, X, Trash2 } from 'lucide-react';

const EXT_ICONS = {
  '.pdf': '📕', '.txt': '📄', '.csv': '📊', '.md': '📝',
  '.docx': '📘', '.pptx': '📙', '.xlsx': '📗',
};

export default function UploadCenter() {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  const { data: uploadStats, refresh: refreshUpload } = usePolling(api.getUploadStats, 5000);
  const { data: dbStats, refresh: refreshDb } = usePolling(api.getStats, 5000);
  const { data: files, refresh: refreshFiles } = usePolling(api.getFiles, 5000);

  const [selectedFiles, setSelectedFiles] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [deletingFile, setDeletingFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
    setResults(null);
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = Array.from(e.dataTransfer.files);
    if (dropped.length) {
      setSelectedFiles(dropped);
      setResults(null);
    }
  }, []);

  const handleUpload = async () => {
    if (!selectedFiles.length) return;
    setProcessing(true);
    setResults(null);
    try {
      const res = await api.uploadFiles(selectedFiles);
      setResults(res.results);
      setSelectedFiles([]);
      refreshUpload();
      refreshDb();
      refreshFiles();
    } catch (e) {
      setResults([{ filename: 'Upload', status: 'error', error: e.message }]);
    } finally {
      setProcessing(false);
    }
  };

  const handleDelete = async (filename) => {
    if (!confirm(`Remove "${filename}" from the knowledge base?\n\nThis will delete the file and rebuild the vector index.`)) return;
    setDeletingFile(filename);
    try {
      await api.deleteFile(filename);
      refreshUpload();
      refreshDb();
      refreshFiles();
    } catch (e) {
      alert(`Failed to delete: ${e.message}`);
    } finally {
      setDeletingFile(null);
    }
  };

  return (
    <div>
      <PageHeader icon="📁" title="Upload Center" subtitle="Upload and manage your knowledge base documents" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <MetricCard icon="📄" value={uploadStats?.total_files ?? '—'} label="Files Uploaded" />
        <MetricCard icon="💾" value={uploadStats ? `${uploadStats.total_size_mb} MB` : '—'} label="Total Size" />
        <MetricCard icon="🧩" value={dbStats?.total_chunks ?? '—'} label="Total Chunks" />
        <MetricCard icon="📊" value={dbStats?.total_pages ?? '—'} label="Total Pages" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <div className="lg:col-span-2 glass-card">
          <h3 className={`text-base font-semibold mb-4 ${dark ? 'text-white' : 'text-slate-800'}`}>
            📤 Upload Documents
          </h3>

          <div
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            className={`relative border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all
              ${dragOver ? 'border-indigo-500 bg-indigo-500/10'
                : dark ? 'border-slate-700 hover:border-indigo-500/40 hover:bg-slate-800/30'
                : 'border-slate-300 hover:border-indigo-400 hover:bg-indigo-50/50'}`}
            onClick={() => document.getElementById('file-input').click()}
          >
            <Upload className={`mx-auto mb-3 ${dark ? 'text-slate-500' : 'text-slate-400'}`} size={36} />
            <p className={`text-sm font-medium ${dark ? 'text-slate-300' : 'text-slate-600'}`}>
              Drag and drop your documents or click to browse
            </p>
            <p className={`text-xs mt-1 ${dark ? 'text-slate-600' : 'text-slate-400'}`}>
              PDF, DOCX, PPTX, XLSX, TXT, CSV, Markdown
            </p>
            <input id="file-input" type="file" multiple accept=".pdf,.txt,.csv,.md,.docx,.pptx,.xlsx"
              className="hidden" onChange={handleFileChange} />
          </div>

          {selectedFiles.length > 0 && (
            <div className="mt-4 space-y-2">
              {selectedFiles.map((f, i) => (
                <div key={i} className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm
                  ${dark ? 'bg-slate-800/50 text-slate-300' : 'bg-slate-50 text-slate-600'}`}>
                  <FileText size={16} className="text-indigo-500 shrink-0" />
                  <span className="flex-1 truncate">{f.name}</span>
                  <span className={`text-xs ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                    {(f.size / 1024 / 1024).toFixed(2)} MB
                  </span>
                  <button onClick={() => setSelectedFiles(prev => prev.filter((_, j) => j !== i))}
                    className={`transition ${dark ? 'text-slate-500 hover:text-red-400' : 'text-slate-400 hover:text-red-500'}`}>
                    <X size={14} />
                  </button>
                </div>
              ))}
              <button onClick={handleUpload} disabled={processing}
                className="w-full mt-2 py-2.5 rounded-lg text-sm font-semibold text-white
                  bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500
                  disabled:opacity-50 disabled:cursor-not-allowed transition-all
                  flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/20">
                {processing ? <><Loader2 size={16} className="animate-spin" /> Processing...</> : <>🚀 Process and Index</>}
              </button>
            </div>
          )}

          {results && (
            <div className="mt-4 space-y-2">
              {results.map((r, i) => (
                <div key={i} className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm border
                  ${r.status === 'success'
                    ? dark ? 'bg-emerald-900/20 text-emerald-300 border-emerald-500/20' : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : dark ? 'bg-red-900/20 text-red-300 border-red-500/20' : 'bg-red-50 text-red-700 border-red-200'}`}>
                  {r.status === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
                  <span className="flex-1">{r.filename}</span>
                  <span className="text-xs opacity-75">
                    {r.status === 'success' ? `${r.chunk_count} chunks` : r.error}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-4">
          <div className="glass-card">
            <h4 className={`text-sm font-semibold mb-3 ${dark ? 'text-white' : 'text-slate-800'}`}>ℹ️ Supported Formats</h4>
            <div className={`text-sm space-y-1.5 ${dark ? 'text-slate-400' : 'text-slate-500'}`}>
              {[['📕','PDF'],['📘','Word (.docx)'],['📙','PowerPoint (.pptx)'],
                ['📗','Excel (.xlsx)'],['📄','Plain Text'],['📊','CSV'],['📝','Markdown']
              ].map(([icon, label]) => <div key={label} className="flex items-center gap-2">{icon} {label}</div>)}
            </div>
          </div>
          <div className="glass-card">
            <h4 className={`text-sm font-semibold mb-3 ${dark ? 'text-white' : 'text-slate-800'}`}>🔧 Pipeline</h4>
            <div className={`text-xs space-y-2 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
              {['Load','Extract','Chunk','Embed','Index'].map((step, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className={`w-5 h-5 rounded-full text-[10px] flex items-center justify-center font-bold shrink-0
                    ${dark ? 'bg-indigo-600/30 text-indigo-400' : 'bg-indigo-100 text-indigo-600'}`}>{i+1}</span>
                  {step}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card">
        <div className="flex items-center justify-between mb-4">
          <h3 className={`text-base font-semibold ${dark ? 'text-white' : 'text-slate-800'}`}>📚 Indexed Documents</h3>
          {files?.length > 0 && (
            <span className={`text-xs px-2 py-1 rounded-full ${dark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'}`}>
              {files.length} file{files.length !== 1 ? 's' : ''}
            </span>
          )}
        </div>

        {deletingFile && (
          <div className={`flex items-center gap-3 px-4 py-3 rounded-lg mb-3 text-sm border
            ${dark ? 'bg-amber-900/20 text-amber-300 border-amber-500/20' : 'bg-amber-50 text-amber-700 border-amber-200'}`}>
            <Loader2 size={16} className="animate-spin shrink-0" />
            Removing <strong className="mx-1">{deletingFile}</strong> and rebuilding index…
          </div>
        )}

        {files?.length > 0 ? (
          <div className="space-y-2">
            {files.map((f, i) => (
              <div key={i} className={`group flex items-center gap-3 px-4 py-3 rounded-xl transition-all border
                ${dark ? 'bg-slate-800/30 hover:bg-slate-800/60 border-transparent hover:border-slate-700/50'
                : 'bg-slate-50 hover:bg-white border-transparent hover:border-slate-200 hover:shadow-sm'}`}>
                <span className="text-xl shrink-0">{EXT_ICONS[f.extension] || '📄'}</span>
                <div className="flex-1 min-w-0">
                  <div className={`text-sm font-medium truncate ${dark ? 'text-slate-200' : 'text-slate-700'}`}>{f.name}</div>
                  <div className={`text-xs mt-0.5 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                    {f.size_mb} MB • {f.extension.toUpperCase()}
                  </div>
                </div>
                <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium shrink-0
                  ${dark ? 'bg-emerald-900/40 text-emerald-400' : 'bg-emerald-100 text-emerald-700'}`}>
                  Indexed
                </span>
                <button onClick={() => handleDelete(f.name)} disabled={deletingFile !== null}
                  title="Remove from knowledge base"
                  className={`ml-1 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-all disabled:cursor-not-allowed
                    ${dark ? 'text-slate-600 hover:text-red-400 hover:bg-red-900/30' : 'text-slate-400 hover:text-red-600 hover:bg-red-50'}`}>
                  {deletingFile === f.name ? <Loader2 size={15} className="animate-spin" /> : <Trash2 size={15} />}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <span className="text-4xl">📭</span>
            <p className={`mt-3 text-sm ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
              No documents uploaded yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
