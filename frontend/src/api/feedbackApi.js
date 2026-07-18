import axios from 'axios';

const FEEDBACK_API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export default {
  submit(feedback) {
    return axios.post(`${FEEDBACK_API_BASE}/feedback/`, feedback);
  },
};
