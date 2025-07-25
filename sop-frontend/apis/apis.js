import axios from 'axios';

const api = axios.create({
  baseURL: 'http://<YOUR_BACKEND_IP>:5000', // replace with your backend IP or localhost
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
