import axios from 'axios';

const CHAT_API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export default {
  ask(question, sessionId) {
    return axios.post(`${CHAT_API_BASE}/chat/`, { question, session_id: sessionId });
  },
};
