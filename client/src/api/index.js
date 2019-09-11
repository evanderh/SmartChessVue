const games = [
  {
    id: '1',
    fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
  },
  {
    id: '2',
    fen: 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R',
  },
];

export default {
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
