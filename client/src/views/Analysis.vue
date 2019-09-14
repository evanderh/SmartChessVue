<template>
  <div class="row">

    <div class="col">
      <div id="board" class="blue merida">
        <div class="cg-wrap" ref="board"></div>
      </div>
    </div>

    <div class="col">
      <div id="history">
        <ul>
          <li
            v-for="mv in history"
            :key="`${mv.ply}${mv.color}`">
            {{ mv.san }}
          </li>
        </ul>
      </div>
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
    ...mapState('analysis', ['fen', 'game', 'history']),
  },
  mounted() {
    this.boardOptions()
      .then((opts) => {
        const options = this.addAfterMove(opts);
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

    addAfterMove(options) {
      return {
        ...options,
        movable: {
          ...options.movable,
          events: { after: this.afterMove },
        },
      };
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

#board {
  padding: 64px;
  border: 1px solid black;
}

#history {
  margin-top: 20px;
}
</style>
