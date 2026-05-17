import { useState, useRef, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import { api } from '../api/client';
import PageHeader from '../components/PageHeader';
import { Send, Loader2, Bot, User, FileText, Settings2 } from 'lucide-react';

export default function AIAssistant() {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [topK, setTopK] = useState(5);
  const [showCitations, setShowCitations] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    const q = input.trim();
    if (!q || loading) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: q }]);
    setLoading(true);

    try {
      const result = await api.ask(q, topK);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.answer,
        citations: result.citations,
        retrieval_ms: result.retrieval_latency_ms,
        total_ms: result.total_latency_ms,
        chunks: result.chunks_retrieved,
      }]);
    } catch (e) {
      const msg = e.message || 'Unknown error';
      const isRateLimit = msg.includes('limit') || msg.includes('429');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: isRateLimit
          ? `⏳ Groq API daily token limit reached.\n\n${msg}\n\nPlease wait a few minutes and try again, or the limit resets daily.`
          : `❌ ${msg}`,
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center justify-between mb-4">
        <PageHeader icon="🤖" title="AI Assistant" subtitle="Ask questions about your uploaded documents" />
        <button onClick={() => setShowSettings(s => !s)}
          className={`p-2 rounded-lg transition ${dark ? 'hover:bg-slate-800 text-slate-400' : 'hover:bg-slate-200 text-slate-500'}`}>
          <Settings2 size={18} />
        </button>
      </div>

      {/* Settings */}
      {showSettings && (
        <div className={`glass-card mb-4 flex items-center gap-6`}>
          <label className={`flex items-center gap-2 text-sm ${dark ? 'text-slate-300' : 'text-slate-600'}`}>
            Top-K:
            <input type="range" min={1} max={15} value={topK}
              onChange={e => setTopK(Number(e.target.value))}
              className="w-24 accent-indigo-500" />
            <span className="font-mono text-xs w-4">{topK}</span>
          </label>
          <label className={`flex items-center gap-2 text-sm cursor-pointer ${dark ? 'text-slate-300' : 'text-slate-600'}`}>
            <input type="checkbox" checked={showCitations}
              onChange={e => setShowCitations(e.target.checked)}
              className="accent-indigo-500" />
            Show Citations
          </label>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center max-w-sm">
              <div className={`w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center
                bg-gradient-to-br from-indigo-600/20 to-purple-600/20 border
                ${dark ? 'border-indigo-500/20' : 'border-indigo-200'}`}>
                <Bot size={36} className="text-indigo-500" />
              </div>
              <p className={`text-xl font-semibold mb-1 ${dark ? 'text-slate-200' : 'text-slate-700'}`}>
                Ask your knowledge base
              </p>
              <p className={`text-sm ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                Ask anything about your uploaded documents. The AI will search and synthesize answers with citations.
              </p>
              <div className="mt-4 flex flex-wrap gap-2 justify-center">
                {['What are the key findings?', 'Summarize the main topics', 'List all requirements'].map(q => (
                  <button key={q} onClick={() => setInput(q)}
                    className={`text-xs px-3 py-1.5 rounded-full border transition
                      ${dark ? 'border-slate-700 text-slate-400 hover:border-indigo-500/40 hover:text-indigo-400' : 'border-slate-200 text-slate-500 hover:border-indigo-300 hover:text-indigo-600'}`}>
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0
                ${dark ? 'bg-indigo-600/30' : 'bg-indigo-100'}`}>
                <Bot size={16} className="text-indigo-500" />
              </div>
            )}
            <div className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed
              ${msg.role === 'user'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-br-md'
                : dark
                  ? 'bg-slate-800/80 text-slate-200 rounded-bl-md border border-slate-700/50'
                  : 'bg-white text-slate-700 rounded-bl-md border border-slate-200 shadow-sm'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>

              {/* Citations */}
              {msg.role === 'assistant' && showCitations && msg.citations?.length > 0 && (
                <div className={`mt-3 pt-3 border-t space-y-2
                  ${dark ? 'border-slate-700' : 'border-slate-200'}`}>
                  <div className={`text-xs font-semibold ${dark ? 'text-indigo-400' : 'text-indigo-600'}`}>
                    📎 Sources Referenced
                  </div>
                  {msg.citations.map((c, j) => (
                    <div key={j} className={`text-xs rounded-lg px-3 py-2
                      ${dark ? 'bg-slate-900/60' : 'bg-slate-50'}`}>
                      <div className="flex items-center justify-between">
                        <span className="font-medium flex items-center gap-1">
                          <FileText size={12} /> [{j + 1}] {c.source}
                        </span>
                        <span className={dark ? 'text-slate-500' : 'text-slate-400'}>
                          Page {c.page} • {c.score?.toFixed(4)}
                        </span>
                      </div>
                      <div className={`mt-1 ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                        {c.chunk_preview}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Perf bar */}
              {msg.role === 'assistant' && msg.retrieval_ms != null && (
                <div className={`mt-2 text-[10px] flex gap-3
                  ${dark ? 'text-slate-500' : 'text-slate-400'}`}>
                  <span>⚡ {msg.retrieval_ms}ms</span>
                  <span>🕐 {msg.total_ms}ms</span>
                  <span>📦 {msg.chunks} chunks</span>
                </div>
              )}
            </div>
            {msg.role === 'user' && (
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0
                ${dark ? 'bg-purple-600/30' : 'bg-purple-100'}`}>
                <User size={16} className="text-purple-500" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 animate-fade-in-up">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0
              ${dark ? 'bg-indigo-600/30' : 'bg-indigo-100'}`}>
              <Bot size={16} className="text-indigo-500" />
            </div>
            <div className={`rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-2
              ${dark ? 'bg-slate-800/80 text-slate-400' : 'bg-white text-slate-500 border border-slate-200'}`}>
              <span className="flex gap-1">
                {[0,1,2].map(i => (
                  <span key={i} className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </span>
              <span className="text-sm">Thinking…</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className={`mt-4 flex gap-2 p-3 rounded-xl border transition-all
        ${dark ? 'bg-slate-800/60 border-slate-700/50 focus-within:border-indigo-500/40' : 'bg-white border-slate-200 shadow-sm focus-within:border-indigo-300 focus-within:shadow-md'}`}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()}
          placeholder="Ask anything about your documents…"
          disabled={loading}
          className={`flex-1 bg-transparent outline-none text-sm
            ${dark ? 'text-slate-200 placeholder:text-slate-600' : 'text-slate-800 placeholder:text-slate-400'}`}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="px-4 py-1.5 rounded-lg text-sm font-medium bg-gradient-to-r from-indigo-600 to-purple-600
            text-white disabled:opacity-40 btn-glow transition flex items-center gap-1.5"
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
          Send
        </button>
      </div>
    </div>
  );
}
