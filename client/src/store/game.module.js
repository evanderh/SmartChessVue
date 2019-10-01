import Chess from 'chess.js';

export default {

  namespaced: true,

  state: {
    // Game state used for display
    displayGame: new Chess(),
    // Game state of current game
    currentGame: new Chess(),
  },

  mutations: {
    move(state, move) {
      // Make the move on the displayed board
      state.displayGame.move({ from: move.from, to: move.to, promotion: 'q' });

      // Reload with new pgn
      const pgn = state.displayGame.pgn();
      state.displayGame = new Chess();
      state.displayGame.load_pgn(pgn);
      state.currentGame = new Chess();
      state.currentGame.load_pgn(pgn);
    },

    gotoStart(state) {
      state.displayGame = new Chess();
    },

    gotoCurrent(state) {
      state.displayGame = new Chess();
      state.displayGame.load_pgn(state.currentGame.pgn());
    },

    gotoPrevious(state) {
      const moves = state.displayGame.history();
      moves.pop();
      state.displayGame = new Chess();
      moves.forEach(move => state.displayGame.move(move));
    },

    gotoNext(state) {
      const pgn = state.displayGame.pgn();
      const move = state.currentGame.history()[state.displayGame.history().length];
      state.displayGame = new Chess();
      state.displayGame.load_pgn(pgn);
      state.displayGame.move(move);
    },
  },

  getters: {
    history(state) {
      return state.currentGame.history({ verbose: true });
    },

    pgn(state) {
      return state.currentGame.pgn();
    },

    fen(state) {
      return state.currentGame.fen();
    },

    currentSTM(state) {
      return (state.displayGame.turn() === 'w') ? 'white' : 'black';
    },

    currentFEN(state) {
      return state.displayGame.fen();
    },

    currentMoves(state) {
      const dests = {};
      state.displayGame.SQUARES.forEach((s) => {
        const ms = state.displayGame.moves({ square: s, verbose: true });
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

  },

};
