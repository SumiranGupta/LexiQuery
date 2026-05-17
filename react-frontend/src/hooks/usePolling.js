import { useState, useEffect, useRef } from 'react';

export function usePolling(fetcher, intervalMs = 5000) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const mountedRef = useRef(true);

  const refresh = async () => {
    const timeout = new Promise((_, reject) =>
      setTimeout(() => reject(Object.assign(new Error('timeout'), { name: 'TimeoutError' })), 8000)
    );
    try {
      const result = await Promise.race([fetcher(), timeout]);
      if (mountedRef.current) {
        setData(result);
        setError(null);
      }
    } catch (e) {
      // Silently swallow timeouts (backend busy); show other errors
      if (mountedRef.current && e.name !== 'TimeoutError') setError(e.message);
    } finally {
      if (mountedRef.current) setLoading(false);
    }
  };

  useEffect(() => {
    mountedRef.current = true;
    refresh();
    const id = setInterval(refresh, intervalMs);
    return () => { mountedRef.current = false; clearInterval(id); };
  }, [intervalMs]);

  return { data, error, loading, refresh };
}
