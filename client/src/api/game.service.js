import helpers from '../helpers';
import logout from './user.service';

const { authHeader } = helpers;
const GAME_API = 'http://localhost:5000/api';

function handleResponse(response) {
  return response.text().then((text) => {
    const data = text && JSON.parse(text);

    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        logout();
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

  return fetch(`${GAME_API}/game`, requestOptions).then(handleResponse);
}

function getGame(id) {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  };

  return fetch(`${GAME_API}/game/${id}`, requestOptions).then(handleResponse);
}

function getGames() {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  };

  return fetch(`${GAME_API}/game`, requestOptions).then(handleResponse);
}

export default {
  createGame,
  getGame,
  getGames,
};
