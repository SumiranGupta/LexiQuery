import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import UploadCenter from './pages/UploadCenter';
import AIAssistant from './pages/AIAssistant';
import QueryHistory from './pages/QueryHistory';
import SystemStatus from './pages/SystemStatus';

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadCenter />} />
            <Route path="/assistant" element={<AIAssistant />} />
            <Route path="/history" element={<QueryHistory />} />
            <Route path="/system" element={<SystemStatus />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
