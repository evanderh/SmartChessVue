<template>
  <div>
    <p>Your account</p>
    <div>
      <p>Your games</p>
      <p>{{ games }}</p>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: 'account',
  data() {
    return {
      games: null,
    };
  },
  created() {
    api.game.getGames()
      .then((response) => {
        this.games = response;
      });
  },
};
</script>
