<template>
  <div v-if="startfen">
    <Board
      :startfen="startFEN"
    />
  </div>

  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: 'game',
  components: {
    Board,
  },
  data() {
    return {
      id: null,
    };
  },
  created() {
    this.loadGame();
  },
  methods: {
    loadGame() {
      const gameID = this.$route.params.id;
      api.game.getGame(gameID)
        .then((response) => {
          console.log(response);
        });
    },
  },
  watch: {
    $route() {
      this.loadGame();
    },
  },
};
</script>

<style lang="scss">
@import '../assets/css/chessground.css';
@import '../assets/css/theme.css';
</style>
