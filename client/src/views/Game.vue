<template>
    <div class="blue merida">
        <div class="cg-board-wrap" ref="board"></div>
        <br>
    </div>
</template>

<script>
import Chess from 'chess.js';
import { Chessground } from 'chessground';

export default {
  name: 'game',
  methods: {
    loadGame() {
      this.board = Chessground(this.$refs.board, {
        orientation: 'white',
      });
    },
  },
  mounted() {
    this.loadGame();
  },
  data() {
    return {
      board: null,
      game: new Chess(),
    };
  },
};
</script>

<style>
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';
</style>
