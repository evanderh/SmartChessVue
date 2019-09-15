import Chess from 'chess.js';

export default {

  namespaced: true,

  state: {
    game: new Chess(),
  },

  mutations: {
    move(state, move) {
      // Make the move on the board
      state.game.move({ from: move.from, to: move.to, promotion: 'q' });
      // Force game to be reactive by reloading pgn
      const pgn = state.game.pgn();
      state.game = new Chess();
      state.game.load_pgn(pgn);
    },
  },

  getters: {
    history(state) {
      return state.game.history({ verbose: true });
    },

    stm(state) {
      return (state.game.turn() === 'w') ? 'white' : 'black';
    },

    fen(state) {
      return state.game.fen();
    },

    boardOptions(state, getters) {
      const dests = {};
      state.game.SQUARES.forEach((s) => {
        const ms = state.game.moves({ square: s, verbose: true });
        if (ms.length) {
          dests[s] = ms.map(m => m.to);
        }
      });

      return {
        fen: getters.fen,
        turnColor: getters.stm,
        movable: {
          free: false,
          color: getters.stm,
          dests,
        },
      };
    },
  },

  actions: {
    makeMove({ state, commit }, { from, to }) {
      const moves = state.game.moves({ verbose: true });
      const move = moves.find(mv => (mv.from === from) && (mv.to === to));
      commit('move', move);
      return move;
    },
  },
};
