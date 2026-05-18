// In production (Vercel), set VITE_API_BASE_URL to your Render backend URL.
// Locally, leave it unset — the Vite dev proxy handles /api/* automatically.
const BASE = (import.meta.env.VITE_API_BASE_URL || '') + '/api';

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  getStats:       ()           => request('/stats'),
  getUploadStats: ()           => request('/upload-stats'),
  getTopSources:  (limit = 5)  => request(`/top-sources?limit=${limit}`),
  getDocuments:   ()           => request('/documents'),
  getFiles:       ()           => request('/files'),
  getQueries:     (limit = 50) => request(`/queries?limit=${limit}`),
  getHealth:      ()           => request('/health'),

  ask: (question, topK = 5) =>
    request('/ask', {
      method: 'POST',
      body: JSON.stringify({ question, top_k: topK }),
    }),

  uploadFiles: (files) => {
    const form = new FormData();
    files.forEach(f => form.append('files', f));
    return fetch(`${BASE}/upload`, { method: 'POST', body: form })
      .then(r => { if (!r.ok) throw new Error(`Upload failed: ${r.statusText}`); return r.json(); });
  },

  deleteFile:   (name) => request(`/files/${encodeURIComponent(name)}`, { method: 'DELETE' }),
  resetSystem:  ()     => request('/reset', { method: 'POST' }),
  resetQueries: ()     => request('/reset-queries', { method: 'POST' }),
};
