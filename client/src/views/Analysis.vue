<template>
  <div class="analysis">
    <Board />
  </div>
</template>

<script>
import Board from '@/components/Board.vue';
import api from '@/api';

export default {
  name: 'Analysis',
  components: {
    Board,
  },
  data() {
    return {
      gameID: null,
      startFEN: null,
    };
  },
  created() {
    const gameID = 1;
    api.game.getGame(gameID)
      .then((response) => {
        this.gameID = response.id;
        this.startFEN = response.fen;
      });
  },
};
</script>
