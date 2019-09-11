<template>
  <div v-if="fen">
    <Board
      :startfen="fen"
    ></Board>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
// @ is an alias to /src
import Board from '@/components/Board.vue';
import api from '@/api';

export default {
  name: 'game',
  components: {
    Board,
  },
  data() {
    return {
      id: null,
      fen: null,
    };
  },
  methods: {
    getGame() {
      api.getGame(this.$route.params.id)
        .then((response) => {
          this.id = response.id;
          this.fen = response.fen;
        });
    },
  },
  created() {
    this.getGame();
  },
};
</script>
