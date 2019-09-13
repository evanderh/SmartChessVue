<template>
  <div class="home">
    <button v-on:click="playGame">Play a Game!</button>
  </div>
</template>

<script>
// @ is an alias to /src
import api from '@/api';

export default {
  name: 'home',
  methods: {
    // Play game button handler
    playGame() {
      api.game.createGame()
        .then((gameID) => {
          this.$router.push({ name: 'Game', params: { id: gameID } });
        });
    },
  },
};
</script>
