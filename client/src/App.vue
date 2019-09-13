<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">BenderChess</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <div class="jumbotron">
      <div class="container">
        <div class="row">
          <div class="col-sm-6 offset-sm-3">
            <div v-if="alert.message" :class="`alert ${alert.type}`">{{alert.message}}</div>
            <router-view/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'app',
  computed: {
    ...mapState({
      alert: state => state.alert,
    }),
  },
  methods: {
    ...mapActions({
      clearAlert: 'alert/clear',
    }),
  },
  watch: {
    $route() {
      this.clearAlert();
    },
  },
};
</script>
