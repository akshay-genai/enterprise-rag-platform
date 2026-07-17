import { useState } from 'react';
import chatApi from '../api/chatApi';

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendMessage = async (question) => {
    const userMessage = { id: Date.now(), role: 'user', content: question };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setError('');

    try {
      const response = await chatApi.ask(question);
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response?.data?.answer || 'No answer returned by the server.',
        sources: response?.data?.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || 'Unable to get answer.');
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, error, sendMessage };
}
