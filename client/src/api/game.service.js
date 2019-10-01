import helpers from '../helpers';
import user from './user.service';

const { authHeader } = helpers;
const GAME_API = 'http://localhost:5000/api';

function handleResponse(response) {
  return response.text().then((text) => {
    const data = text && JSON.parse(text);

    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        user.logout();
      }

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}

function createGame() {
  const requestOptions = {
    method: 'POST',
    headers: authHeader(),
  };

  return fetch(`${GAME_API}/games`, requestOptions).then(handleResponse);
}

function getGame(id) {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  };

  return fetch(`${GAME_API}/games/${id}`, requestOptions).then(handleResponse);
}

function getGames() {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  };

  return fetch(`${GAME_API}/games`, requestOptions).then(handleResponse);
}

export default {
  createGame,
  getGame,
  getGames,
};
