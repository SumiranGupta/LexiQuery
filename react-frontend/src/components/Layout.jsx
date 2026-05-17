import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { useTheme } from '../context/ThemeContext';

export default function Layout() {
  const { theme } = useTheme();
  const dark = theme === 'dark';

  return (
    <div
      className="flex h-screen overflow-hidden"
      style={{
        background: dark
          ? 'linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0f172a 100%)'
          : 'linear-gradient(135deg, #f0f4ff 0%, #e8ecf4 50%, #f8fafc 100%)',
        color: dark ? '#f1f5f9' : '#0f172a',
      }}
    >
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6 lg:p-8">
        <Outlet />
      </main>
    </div>
  );
}
