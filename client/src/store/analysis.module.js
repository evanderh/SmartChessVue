import Chess from 'chess.js';

export default {

  namespaced: true,

  state: {
    game: new Chess(),
    fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    stm: 'white',
    history: [],
  },

  mutations: {
    move(state, move) {
      state.game.move({ from: move.from, to: move.to, promotion: 'q' });
      state.fen = state.game.fen();
      state.stm = (state.game.turn() === 'w') ? 'white' : 'black';
      state.history.push(move);
    },
  },

  actions: {
    makeMove({ state, commit }, { from, to }) {
      const moves = state.game.moves({ verbose: true });
      const move = moves.find(mv => (mv.from === from) && (mv.to === to));
      commit('move', move);
      return move;
    },

    boardOptions({ state }) {
      const dests = {};
      state.game.SQUARES.forEach((s) => {
        const ms = state.game.moves({ square: s, verbose: true });
        if (ms.length) {
          dests[s] = ms.map(m => m.to);
        }
      });

      return {
        fen: state.fen,
        turnColor: state.stm,
        movable: {
          free: false,
          color: state.stm,
          dests,
        },
      };
    },
  },
};
