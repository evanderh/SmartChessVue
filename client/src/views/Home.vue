<template>
  <div class="home">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">{{ heroTxt }}</h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="card"
          v-for="choice in gameChoices"
          v-bind:key="choice.msg">
            <PlayGame
              v-bind:options="choice"
            ></PlayGame>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
// @ is an alias to /src
import PlayGame from '@/components/PlayGame.vue';
// import axios from 'axios';

export default {
  name: 'home',
  components: {
    PlayGame,
  },
  data() {
    return {
      heroTxt: 'Play a game!',
      gameChoices: [
        { timeControl: 1, increment: 0, msg: '1+0' },
        { timeControl: 3, increment: 0, msg: '3+0' },
        { timeControl: 5, increment: 0, msg: '5+0' },
      ],
    };
  },
};
</script>
