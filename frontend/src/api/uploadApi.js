import axios from 'axios';

export default {
  upload(file) {
    const formData = new FormData();
    formData.append('file', file);

    return axios.post('/upload/', formData);
  },
};
