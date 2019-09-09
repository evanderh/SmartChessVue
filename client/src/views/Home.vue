<template>
  <div class="home">
    <PlayGame msg="Play a game"/>
  </div>
</template>

<script>
// @ is an alias to /src
import PlayGame from '@/components/PlayGame.vue';

export default {
  name: 'home',
  components: {
    PlayGame,
  },
};
</script>
