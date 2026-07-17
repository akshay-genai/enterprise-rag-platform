import axios from 'axios';

export default {
  ask(question) {
    return axios.post('/chat/', { question });
  },
};
