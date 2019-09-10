<template>
  <div class="card-content">
    <p class="title"></p>
    <router-link to="/game">{{ options.msg }}</router-link>
  </div>
</template>

<script>
export default {
  name: 'PlayGame',
  props: {
    options: Object,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card-content {
  color: #42b983;
}
</style>
