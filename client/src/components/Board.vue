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
    fen: {
      type: String,
      default: '',
    },
  },
  computed: {

  },
  data() {
    return {
      board: null,
      chess: new Chess(),
    };
  },
  methods: {
    createBoard() {
      this.chess.load(this.fen);
      this.drawBoard();
    },
    drawBoard() {
      console.log(this.legalMoves());
      this.board = Chessground(this.$refs.board, this.boardOpts());
    },
    makeMove(orig, dest, meta) {
      // console.log(orig, dest, meta);
      this.chess.move({ from: orig, to: dest });

      this.board.set({
        turnColor: this.stm(),
        movable: this.movableOpts(),
      });
    },
    boardOpts() {
      return {
        fen: this.fen,
        turnColor: this.stm(),
        movable: this.movableOpts(),
      };
    },
    legalMoves() {
      const dests = {};
      this.chess.SQUARES.forEach(s => {
        const ms = this.chess.moves({square: s, verbose: true});
        if (ms.length)
          dests[s] = ms.map(m => m.to);
      });
      return dests;
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
    stm() {
      return (this.chess.turn() === 'w') ? 'white' : 'black';
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
