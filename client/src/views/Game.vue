<template>
  <div v-if="startFEN">
    <Board
      :startfen="startFEN"
    ></Board>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
import Board from '@/components/Board.vue';
import api from '@/api';

export default {
  name: 'game',
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
    const gameID = this.$route.params.id;
    api.game.getGame(gameID)
      .then((response) => {
        this.gameID = response.id;
        this.startFEN = response.fen;
      });
  },
};
</script>
