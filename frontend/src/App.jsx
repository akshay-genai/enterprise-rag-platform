import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import ChatPage from './pages/ChatPage';
import UploadPage from './pages/UploadPage';
import AdminPage from './pages/AdminPage';
import LoginPage from './pages/LoginPage';
import { ChatProvider } from './context/ChatContext';

export default function App() {
  return (
    <ChatProvider>
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <Box sx={{ display: 'flex', flex: 1 }}>
          <Sidebar />
          <Box component="main" sx={{ flex: 1, p: 3, bgcolor: '#f5f7fb' }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="/login" element={<LoginPage />} />
            </Routes>
          </Box>
        </Box>
      </Box>
    </ChatProvider>
  );
}
