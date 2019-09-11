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
  // watch: {
  //   fen:
  // },
  computed: {
    options() {
      return {
        fen: this.fen,
      };
    },
  },
  data() {
    return {
      board: null,
      chess: new Chess(),
    };
  },
  methods: {
    createBoard() {
      console.log(this.options);
      this.board = Chessground(this.$refs.board, this.options);
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
