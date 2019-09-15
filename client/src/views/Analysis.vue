<template>
  <div class="row">

    <div class="col">
      <div id="board" class="blue merida">
        <div class="cg-wrap" ref="board"></div>
      </div>

      <div id="buttons">
        <button @click="toStart">&lt;&lt;</button>
        <!-- <button @click="previous">&lt;</button> -->
        <!-- <button @click="next">&gt;</button> -->
        <button @click="toCurrent">&gt;&gt;</button>
      </div>
    </div>

    <div class="col">

      <div id="movehistory">
        <p>Move history</p>
        <ul>
          <li
            v-for="(mv, ix) in history"
            :key="`${ix}${mv.color}`">
            {{ mv.san }}
          </li>
        </ul>
      </div>

      <div id="pgn">
        <p>PGN</p>
        <p>{{ pgn }}</p>
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

#buttons {
  margin-top: 20px;
}

#movehistory {
  padding: 20px;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: 0 5px 10px 2px rgba(0, 0, 0, 0.5);
  margin-bottom: 20px;
}

#pgn {
  padding: 20px;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: 0 5px 10px 2px rgba(0, 0, 0, 0.5);
}
</style>


<script>
import { mapActions, mapGetters } from 'vuex';

import { Chessground } from 'chessground';

export default {
  name: 'Analysis',
  data() {
    return {
      board: null,
    };
  },
  computed: {
    ...mapGetters('analysis', ['boardOptions', 'history', 'pgn']),
  },
  mounted() {
    const options = this.addAfterMove(this.boardOptions);
    this.board = Chessground(this.$refs.board, options);
  },
  methods: {
    ...mapActions('analysis', ['makeMove', 'rewindToStart', 'ffToCurrent']),

    toStart() {
      this.rewindToStart();
      this.board.set(this.boardOptions);
    },

    toCurrent() {
      this.ffToCurrent();
      this.board.set(this.boardOptions);
    },

    afterMove(from, to) {
      const move = this.makeMove({ from, to });
      if ('promotion' in move) this.makePromotion(move);
      this.board.set(this.boardOptions);
    },

    // Helper methods
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
