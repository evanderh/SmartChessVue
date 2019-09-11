import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export default {
  fetchUser() {
    return axios.get(`${API_URL}/user/world`);
  },

  fetchGame(id) {
    return axios.get(`${API_URL}/game/${id}`);
  },

  getGameId() {
    return new Promise((resolve, reject) => {
      const gameId = '2';

      if (gameId) {
        resolve(gameId);
      } else {
        reject(Error('No game'));
      }
    });
  },

  getGame(id) {
    return new Promise((resolve, reject) => {
      const game = games.find(g => g.id === id);

      if (game) {
        resolve(game);
      } else {
        reject(Error('Game not found'));
      }
    });
  },
};
