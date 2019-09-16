<template>
  <div class="row">

    <div class="col-md-6">
      <div class="blue merida">
        <div id="board" class="cg-wrap" ref="board"></div>
      </div>

      <div id="buttons">
        <button @click="toStart">&lt;&lt;</button>
        <button @click="toPrevious">&lt;</button>
        <button @click="toNext">&gt;</button>
        <button @click="toCurrent">&gt;&gt;</button>
      </div>

      <div id="movehistory">
        <h6>Move history</h6>
        <p>
          <span
            v-for="(mv, ix) in history"
            :key="`${ix}${mv.color}`">
            {{ mv.san }}
          </span>
        </p>
      </div>
    </div>

    <div class="col-md-6">
      <b-tabs>
        <b-tab title="Analysis" active>
          <div id="engineOutput" class="engineTab">
            <div class="blue merida">
              <div id="engineBoard" class="cg-wrap" ref="engineBoard"></div>
            </div>
          </div>
        </b-tab>

        <b-tab title="Raw">
          <div id="uciOutput" class="engineTab" ref="uciOutputDiv">
            <p
              v-for="(line, ix) in output"
              :key="`${ix}-${line}`">
              {{ line }}
            </p>
          </div>
        </b-tab>

      </b-tabs>
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
      engineBoard: null,
      engineDepth: 0,
      engineTime: 0,
      enginePV: [],
      engineScore: '',
      engineBestMove: null,
      output: [],
      depth: 13,
    };
  },

  created() {
    this.engine = new Lozza();
    const vm = this;
    this.engine.onmessage = e => vm.output.push(e.data);

    this.engine.postMessage('uci');
    this.engine.postMessage('ucinewgame');
    this.search(9);
    this.search(this.depth);
  },

  computed: {
    ...mapState('analysis', ['currentGame']),
    ...mapGetters('analysis', ['boardOptions', 'history', 'currentFEN']),
  },

  watch: {
    currentGame() {
      this.search(this.depth);
    },

    output(output) {
      // Watch the engine output, UCI protocol
      // http://wbec-ridderkerk.nl/html/UCIProtocol.html
      if (output.length > 200) output.shift();

      const newline = output[output.length - 1];
      const words = newline.split(' ');

      const UCIword = words.shift();
      switch (UCIword) {
        case 'bestmove':
          [this.engineBestMove] = words;
          break;

        case 'info':
          break;

        default:
          break;
      }
    },

    engineBestMove(best) {
      console.log(best);
      const orig = best.slice(0, 2);
      const dest = best.slice(2);
      this.mountEngineBoard();
      this.engineBoard.move(orig, dest);
    },
  },

  mounted() {
    const options = this.addAfterMove(this.boardOptions);
    this.board = Chessground(this.$refs.board, options);
    window.addEventListener('resize', () => {
      document.body.dispatchEvent(new Event('chessground.resize'));
    });
    this.mountEngineBoard();
  },

  updated() {
    // Scroll to bottom of uci output
    const output = this.$refs.uciOutputDiv;
    output.scrollTop = output.scrollHeight;
  },

  methods: {
    ...mapActions('analysis', ['makeMove']),
    ...mapMutations('analysis', ['gotoStart', 'gotoCurrent', 'gotoPrevious', 'gotoNext']),

    mountEngineBoard() {
      this.engineBoard = Chessground(this.$refs.engineBoard, {
        viewOnly: true,
        fen: this.currentFEN,
      });
    },

    search(depth) {
      this.engine.postMessage(`position fen ${this.currentFEN}`);
      this.engine.postMessage(`go depth ${depth}`);
    },

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
      // Re-search
      this.engine.postMessage(`position ${this.currentFEN}`);
      this.search(this.depth);
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

<style lang="scss">
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';

#board {
  background-size: cover;
  margin: 20px auto;

  height: 362px;
  width: 362px;

  border: 1px solid black;
  border-radius: 3px;
  box-shadow: 0 1px 3px 1px rgba(0, 0, 0, 0.5);
}

#engineBoard {
  height: 202px;
  width: 202px;
  margin: 10px auto;
  border: 1px solid #b1b4b6;
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
  padding: 5px;
  border: 1px solid #dee2e6;
  border-radius: 2px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.5);
  font-size: 13px;
  margin: 40px;
}

.engineTab {
  padding: 5px;
  border: 1px solid #dee2e6;
  border-top: none;
}

#uciOutput {
  height: 500px;
  overflow: scroll;
}

#uciOutput p {
  white-space: nowrap;
  font-size: 8px;
  margin: 0;
}
</style>
