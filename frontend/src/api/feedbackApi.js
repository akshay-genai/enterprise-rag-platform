import axios from 'axios';

const FEEDBACK_API_BASE = 'http://127.0.0.1:8000';

export default {
  submit(feedback) {
    return axios.post(`${FEEDBACK_API_BASE}/feedback/`, feedback);
  },
};
