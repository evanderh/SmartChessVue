<template>
  <div class="blue merida">
    <div class="cg-wrap" ref="board"></div>
    <br>
  </div>
</template>

<script>
import Chess from 'chess.js';
import { Chessground } from 'chessground';

export default {
  name: 'board',
  props: {
    startfen: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      fen: this.startfen,
      board: null,
      chess: new Chess(),
    };
  },
  methods: {
    createBoard() {
      // Load FEN string into game
      this.chess.load(this.fen);

      // Create board display
      this.board = Chessground(this.$refs.board, {
        fen: this.fen,
        turnColor: this.stm(),
        movable: this.movableOpts(),
      });
    },
    getMove(orig, dest) {
      const moves = this.chess.moves({ verbose: true });
      return moves.find(move => (move.from === orig) && (move.to === dest));
    },
    makeMove(orig, dest) {
      // Get the move details
      const move = this.getMove(orig, dest);

      // Make the move in the game, update FEN
      this.chess.move({ from: orig, to: dest, promotion: 'q' });
      this.fen = this.chess.fen();

      // Update board display
      if ('promotion' in move) {
        this.board.setPieces({
          [move.to]: {
            color: (move.color === 'w') ? 'white' : 'black',
            role: 'queen',
          },
        });
      }
      this.board.set({
        turnColor: this.stm(),
        movable: this.movableOpts(),
      });

      console.log(this.chess.ascii());
    },
    stm() {
      return (this.chess.turn() === 'w') ? 'white' : 'black';
    },
    movableOpts() {
      return {
        free: false,
        color: this.stm(),
        dests: this.legalMoves(),
        events: {
          after: this.makeMove,
        },
      };
    },
    legalMoves() {
      const dests = {};
      this.chess.SQUARES.forEach((s) => {
        const ms = this.chess.moves({ square: s, verbose: true });
        if (ms.length) {
          dests[s] = ms.map(m => m.to);
        }
      });
      return dests;
    },
  },
  mounted() {
    this.createBoard();
  },
};
</script>

<style>
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';
</style>
