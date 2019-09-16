<template>
  <div class="row">

    <div class="col-md-6">
      <div id="board" class="blue merida">
        <div class="cg-wrap" ref="board"></div>
      </div>

      <div id="buttons">
        <button @click="toStart">&lt;&lt;</button>
        <button @click="toPrevious">&lt;</button>
        <button @click="toNext">&gt;</button>
        <button @click="toCurrent">&gt;&gt;</button>
      </div>

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
    </div>

    <div class="col-md-6">

      <div id="analysis">
        <p class="uciLine"
          v-for="(line, ix) in output"
          :key="`${ix}-${line}`">
          {{ line }}
        </p>
      </div>

    </div>

  </div>
</template>

<script>
import {
  mapActions, mapGetters, mapState, mapMutations,
} from 'vuex';

import { Chessground } from 'chessground';
// eslint-disable-next-line
import Lozza from 'worker-loader!../assets/js/lozza';

export default {
  name: 'Analysis',

  data() {
    return {
      board: null,
      engine: null,
      output: [],
    };
  },

  created() {
    const vm = this;
    vm.engine = new Lozza();
    vm.engine.onmessage = e => vm.output.push(e.data);
    vm.engine.postMessage('uci');
    vm.engine.postMessage('ucinewgame');
    vm.engine.postMessage('position startpos');
    vm.engine.postMessage('go depth 10');
  },

  computed: {
    ...mapState('analysis', ['engineLozza', 'engineOutput']),
    ...mapGetters('analysis', ['boardOptions', 'history', 'pgn']),
  },

  mounted() {
    const options = this.addAfterMove(this.boardOptions);
    this.board = Chessground(this.$refs.board, options);
  },

  methods: {
    ...mapActions('analysis', ['makeMove']),
    ...mapMutations('analysis', ['gotoStart', 'gotoCurrent', 'gotoPrevious', 'gotoNext']),


    toStart() {
      this.gotoStart();
      this.board.set(this.boardOptions);
    },

    toCurrent() {
      this.gotoCurrent();
      this.board.set(this.boardOptions);
    },

    toPrevious() {
      this.gotoPrevious();
      this.board.set(this.boardOptions);
    },

    toNext() {
      this.gotoNext();
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

<style>
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';

.uciLine {
  font-size: 8px;
  margin: 0;
}

#board {
  width: 362px;
  padding: 20px;
  margin: auto;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: 0 5px 10px 2px rgba(0, 0, 0, 0.5);
}

#buttons {
  margin: auto;
  width: 320px;
}

#buttons button {
  margin: 10px;
  width: 60px;
}

#movehistory {
  padding: 20px;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: 0 5px 10px 2px rgba(0, 0, 0, 0.5);
  margin-bottom: 20px;
}

#analysis {
  padding: 20px;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: 0 5px 10px 2px rgba(0, 0, 0, 0.5);
}
</style>
