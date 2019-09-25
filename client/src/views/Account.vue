<template>
  <div>
    <p>Your account</p>
    <div>
      <p>Your games</p>
      <ul>
        <li
          v-for="game in games"
          :key="game.id">
          {{ game.fen }}
        </li>
      </ul>
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
