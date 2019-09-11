import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export default {
  fetchUser() {
    return axios.get(`${API_URL}/user/world`);
  },

  fetchGame(id) {
    return axios.get(`${API_URL}/game/${id}`);
  },

  createGame() {
    return axios.post(`${API_URL}/game`);
  },

};
