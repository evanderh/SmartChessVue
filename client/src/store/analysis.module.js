import Chess from 'chess.js';

export default {

  namespaced: true,

  state: {
    game: new Chess(),
    currentGame: new Chess(),
  },

  mutations: {
    move(state, move) {
      // Make the move on the current board
      state.currentGame.move({ from: move.from, to: move.to, promotion: 'q' });
      // Force game to be reactive by reloading pgn
      const pgn = state.currentGame.pgn();
      state.game = new Chess();
      state.game.load_pgn(pgn);
      state.currentGame = new Chess();
      state.currentGame.load_pgn(pgn);
    },

    rewindToStart(state) {
      state.currentGame = new Chess();
    },

    ffToCurrent(state) {
      state.currentGame = new Chess();
      state.currentGame.load_pgn(state.game.pgn());
    },
  },

  getters: {
    history(state) {
      return state.game.history({ verbose: true });
    },

    pgn(state) {
      return state.game.pgn();
    },

    fen(state) {
      return state.game.fen();
    },

    currentSTM(state) {
      return (state.currentGame.turn() === 'w') ? 'white' : 'black';
    },

    currentFEN(state) {
      return state.currentGame.fen();
    },

    currentMoves(state) {
      const dests = {};
      state.currentGame.SQUARES.forEach((s) => {
        const ms = state.currentGame.moves({ square: s, verbose: true });
        if (ms.length) {
          dests[s] = ms.map(m => m.to);
        }
      });
      return dests;
    },

    boardOptions(state, getters) {
      const dests = getters.currentMoves;

      return {
        fen: getters.currentFEN,
        turnColor: getters.currentSTM,
        movable: {
          free: false,
          color: getters.currentSTM,
          dests,
        },
      };
    },
  },

  actions: {
    makeMove({ state, commit }, { from, to }) {
      const moves = state.currentGame.moves({ verbose: true });
      const move = moves.find(mv => (mv.from === from) && (mv.to === to));
      commit('move', move);
      return move;
    },

    rewindToStart({ commit }) {
      commit('rewindToStart');
    },

    ffToCurrent({ commit }) {
      commit('ffToCurrent');
    },
  },
};
