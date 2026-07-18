import { createContext, useContext, useMemo, useState } from 'react';

const ChatContext = createContext(null);

const buildSessionId = () => `session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;

export function ChatProvider({ children }) {
  const [sessionId, setSessionId] = useState(() => buildSessionId());

  const value = useMemo(() => ({ sessionId, setSessionId }), [sessionId]);

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export function useChatContext() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
}
