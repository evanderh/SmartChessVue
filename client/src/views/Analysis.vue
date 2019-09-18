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
            {{ (ix % 2) === 0 ? ((ix/2)+1 + '.') : ''}}
            {{ mv.san }}
          </span>
        </p>
      </div>
    </div>

    <div class="col-md-6">
      <b-tabs>

        <b-tab title="Analysis" active>
          <div id="engineView" class="engineTab">

            <SearchDetails
              :move="engineBestMove" :eval="engineScore"
              :nps="engineNPS" :time="engineTime"
              :depth="engineDepth" :seldepth="engineSelDepth"
              :nodes="engineNodes" :tbhits="engineTBhits" :pv="enginePV" />
            <hr style="margin-bottom:0"/>

            <!-- Search Options -->
            <div class="m-2">
              <b-button squared variant="primary" @click="onSearch" size="sm" >Search</b-button>
              <!-- <b-dropdown text="Mode" variant="outline-secondary" size="sm" class="m-2">
                <b-dropdown-item href="#">Search depth: 8</b-dropdown-item>
              </b-dropdown> -->

              <span>
                <label for="searchDepth" class="m-2">Depth: {{ depth }}</label>
                <b-form-input
                  id="searchDepthInput" class="align-middle"
                  v-model="depth"
                  type="range" min="1" max="20"
                ></b-form-input>
              </span>
            </div>

            <!-- Engine -->
            <div class="blue merida">
              <div id="engineBoard" class="cg-wrap" ref="engineBoard"></div>
            </div>
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
import { Chessground } from 'chessground';
import {
  mapActions, mapGetters, mapState, mapMutations,
} from 'vuex';
import SearchDetails from '@/components/SearchDetails.vue';
import EngineDetails from '@/components/EngineDetails.vue';


export default {
  name: 'Analysis',
  components: {
    SearchDetails,
    EngineDetails,
  },

  data() {
    return {
      depth: 10,
      board: null,
      engine: null,
      engineName: '',
      engineBoard: null,
      engineDepth: 0,
      engineSelDepth: 0,
      engineTime: 0,
      engineNodes: 0,
      enginePV: [],
      engineScore: '0.00',
      engineNPS: 0,
      engineTBhits: 0,
      engineBestMove: null,
      output: [],
    };
  },

  computed: {
    ...mapState('analysis', ['currentGame']),
    ...mapGetters('analysis', ['boardOptions', 'history', 'currentFEN']),
  },

  created() {
    this.engine = new Lozza();
    const vm = this;
    this.engine.onmessage = e => vm.output.push(e.data);

    this.engine.postMessage('uci');
    this.engine.postMessage('ucinewgame');
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

  watch: {
    currentGame() {
      this.search(this.depth);
    },

    output(output) {
      // Watch the engine output, UCI protocol
      // http://wbec-ridderkerk.nl/html/UCIProtocol.html
      while (output.length > 200) output.shift();

      const newline = output[output.length - 1];
      const words = newline.split(' ');

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
              case 'seldepth':
                this.engineSelDepth = parseInt(words.shift(), 10);
                break;

              case 'time':
                this.engineTime = parseInt(words.shift(), 10);
                break;

              case 'nodes':
                this.engineNodes = parseInt(words.shift(), 10);
                break;

              case 'nps':
                this.engineNPS = parseInt(words.shift(), 10);
                break;

              case 'score':
                if (words.shift() === 'cp') this.engineScore = (parseInt(words.shift(), 10) / 100).toFixed(2);
                else this.engineScore = `Mate in ${parseInt(words.shift(), 10) + 1}`;
                break;

              case 'pv':
                this.enginePV = words.slice();
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
      if (depth === 'infinite') this.engine.postMessage(`go ${depth}`);
      this.engine.postMessage(`go depth ${depth}`);
    },

    onSearch() {
      this.engine.postMessage(`position ${this.currentFEN}`);
      this.search(this.depth);
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
  font-family: sans-serif;
  font-size: 14px;
  line-height: 1em;
}

.engineTab h6 {
  font-family: sans-serif;
  font-weight: 600;
}

.engineTab dl, .engineTab dd {
  margin: 0;
}

#searchDepthInput {
  width: 100px;
}

#engineBoard {
  height: 202px;
  width: 202px;
  margin: 10px auto;
  border: 1px solid #b1b4b6;
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
