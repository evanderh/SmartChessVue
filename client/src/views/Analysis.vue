<template>
  <div class="row">
    <!-- Left column -->
    <div class="col-md-6">
      <!-- Main board -->
      <div class="blue merida">
        <div id="board" class="cg-wrap" ref="board"></div>
      </div>

      <!-- Board navigation buttons -->
      <div id="buttons">
        <button @click="toStart">&lt;&lt;</button>
        <button @click="toPrevious">&lt;</button>
        <button @click="toNext">&gt;</button>
        <button @click="toCurrent">&gt;&gt;</button>
      </div>

      <!-- History -->
      <div id="movehistory">
        <p>
          <span
            v-for="(mv, ix) in history"
            :key="`${ix}${mv.color}`">
            {{ mv.san }}
          </span>
        </p>
      </div>
    </div>

    <!-- Right column -->
    <div class="col-md-6">
      <b-tabs>

        <!-- Analysis tab -->
        <b-tab title="Analysis" active>
          <div id="engineView" class="engineTab">

            <!-- Search details -->
            <div id="searchDetails" class="col-10">
              <h6>Search</h6>
              <dl class="row">
                <dt class="col-4">Best move: </dt>
                <dd class="col-8">{{ engineBestMove }}</dd>
              </dl>

              <dl class="row">
                <dt class="col-4">Time: </dt>
                <dd class="col-8">{{ engineTime }}ms</dd>
              </dl>

              <dl class="row">
                <dt class="col-4">Depth:</dt>
                <dd class="col-8">{{ engineDepth }}</dd>
              </dl>

              <dl class="row">
                <dt class="col-4">PV</dt>
                <dd class="col-8">
                  <span
                    v-for="(mv, ix) in enginePV"
                    :key="`${mv}${ix}`">
                    {{ mv }}
                  </span>
                </dd>
              </dl>
            </div>

            <!-- Engine board -->
            <div class="blue merida">
              <div id="engineBoard" class="cg-wrap" ref="engineBoard"></div>
            </div>

            <!-- Engine details/options -->
            <EngineDetails
              :name="engineName" />

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
// eslint-disable-next-line
import Lozza from 'worker-loader!../assets/js/lozza';
import {
  mapActions, mapGetters, mapState, mapMutations,
} from 'vuex';
import { Chessground } from 'chessground';
import EngineDetails from '@/components/EngineDetails.vue';


export default {
  name: 'Analysis',
  components: {
    EngineDetails,
  },

  data() {
    return {
      board: null,
      engine: null,
      engineName: '',
      engineBoard: null,
      engineDepth: 0,
      engineTime: 0,
      engineNodes: 0,
      enginePV: [],
      engineScore: '',
      engineBestMove: null,
      output: [],
      depth: 13,
    };
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
      let words = newline.split(' ');

      const UCIword = words.shift();
      let word = null;
      switch (UCIword) {
        case 'bestmove':
          [this.engineBestMove] = words;
          break;

        case 'id':
          if (words.shift() === 'name') this.engineName = words.join(' ');
          break;

        case 'info':
          // For each info value
          word = words.shift();
          while (word !== undefined) {
            switch (word) {
              case 'depth':
                this.engineDepth = parseInt(words.shift(), 10);
                break;

              case 'time':
                this.engineTime = parseInt(words.shift(), 10);
                break;

              case 'nodes':
                this.engineNodes = parseInt(words.shift(), 10);
                break;

              case 'pv':
                this.enginePV = words;
                words = []; // empty words to exit outer loop
                break;

              default:
                break;
            }
            word = words.shift();
          }

          break;

        default:
          break;
      }
    },

    engineBestMove(best) {
      const orig = best.slice(0, 2);
      const dest = best.slice(2);
      this.drawEngineBoard();
      this.engineBoard.move(orig, dest);
    },

    enginePV(newPV) {
      console.log('pv', newPV[0]);
    },
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

  mounted() {
    const options = this.addAfterMove(this.boardOptions);
    this.board = Chessground(this.$refs.board, options);
    window.addEventListener('resize', () => {
      document.body.dispatchEvent(new Event('chessground.resize'));
    });
    this.engineBoard = Chessground(this.$refs.engineBoard, {
      viewOnly: true,
    });
    this.drawEngineBoard();
  },

  updated() {
    // Scroll to bottom of uci output
    const output = this.$refs.uciOutputDiv;
    output.scrollTop = output.scrollHeight;
  },

  methods: {
    ...mapActions('analysis', ['makeMove']),
    ...mapMutations('analysis', ['gotoStart', 'gotoCurrent', 'gotoPrevious', 'gotoNext']),

    drawEngineBoard() {
      this.engineBoard.set({
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
// Left column
#board {
  background-size: cover;
  margin: 20px auto;
  height: 362px;
  width: 362px;
  border: 1px solid black;
  border-radius: 3px;
  box-shadow: 0 1px 3px 1px rgba(0, 0, 0, 0.5);
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
  width: 320px;
  height: 80px;
  overflow: auto;
  padding: 3px;
  border: 1px solid #dee2e6;
  border-radius: 2px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.5);
  font-size: 12px;
  font-family: sans-serif;
  margin: 20px auto;
}

// Right column

.engineTab {
  padding: 5px;
  border: 1px solid #dee2e6;
  border-top: none;
}

.engineTab h6 {
  font-family: sans-serif;
  font-weight: 600;
}

.engineTab dl {
  margin: 0;
  font-family: sans-serif;
  font-size: 14px;
  line-height: 1em;
}

.engineTab dt {
  margin-bottom: 5px;
}

#engineBoard {
  height: 202px;
  width: 202px;
  margin: 10px auto;
  border: 1px solid #b1b4b6;
}

#searchDetails {
  margin: 10px auto;
  padding: 5px;
  border: 1px solid #dee2e6;
}

#uciOutput {
  height: 500px;
  overflow: scroll;
}

#uciOutput p {
  white-space: nowrap;
  font-size: 12px !important;
  font-family: monospace;
  line-height: 1em;
  margin: 0;
}
</style>
