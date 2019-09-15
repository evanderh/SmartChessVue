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
            v-for="(mv, ix) in history"
            :key="`${ix}${mv.color}`">
            {{ mv }}
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<style>
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';

#board {
  width: 362px;
  padding: 20px;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: 0 5px 10px 2px rgba(0, 0, 0, 0.5);
}
</style>


<script>
import { mapState, mapActions, mapGetters } from 'vuex';

import { Chessground } from 'chessground';

export default {
  name: 'Analysis',
  data() {
    return {
      board: null,
    };
  },
  computed: {
    ...mapState('analysis', ['game']),
    ...mapGetters('analysis', ['boardOptions', 'history']),
  },
  mounted() {
    const options = this.addAfterMove(this.boardOptions);
    this.board = Chessground(this.$refs.board, options);
  },
  methods: {
    ...mapActions('analysis', ['makeMove']),

    afterMove(from, to) {
      const move = this.makeMove({ from, to });
      if ('promotion' in move) this.makePromotion(move);
      this.board.set(this.boardOptions);
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
