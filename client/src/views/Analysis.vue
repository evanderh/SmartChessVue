<template>
  <div class="analysis">
    <div class="blue merida">
      <div class="cg-wrap" ref="board"></div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

import { Chessground } from 'chessground';

export default {
  name: 'Analysis',
  data() {
    return {
      board: null,
    };
  },
  computed: {
    ...mapState('analysis', ['fen', 'game']),
  },
  mounted() {
    this.boardOptions()
      .then((opts) => {
        const options = {
          ...opts,
          movable: {
            ...opts.movable,
            events: { after: this.afterMove }
          },
        };
        this.board = Chessground(this.$refs.board, options);
      });
  },
  methods: {
    ...mapActions('analysis', ['makeMove', 'boardOptions']),

    afterMove(from, to) {
      const move = this.makeMove({ from, to });
      if ('promotion' in move) this.makePromotion(move);
      this.board.set(this.boardOptions());
      this.boardOptions()
        .then((opts) => {
          this.board.set(opts);
        });
    },

    makePromotion(move) {
      this.board.setPieces({
        [move.to]: {
          color: (move.color === 'w') ? 'white' : 'black',
          role: 'queen',
        },
      });
    },
  },
};
</script>

<style>
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';
</style>
