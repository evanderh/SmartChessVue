<template>
  <div id="app">

    <div id="nav">

      <router-link to="/">Smart Chess</router-link>
      <span> | </span>

      <router-link
        v-if="!account.status.loggedIn"
        to="/login">
        Login
      </router-link>
      <router-link
        v-else
        to="/login">
        Logout
      </router-link>
      <span> | </span>

      <button
        @click="newGame">
        New game
      </button>
      <span v-if="account.status.loggedIn"> | </span>

      <router-link
        v-if="account.status.loggedIn"
        to="/account">
        Account
      </router-link>
      <span v-if="account.status.loggedIn"> | </span>

    </div>
    <hr />

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-6 offset-sm-3">
          <div v-if="alert.message" :class="`alert ${alert.type}`">{{alert.message}}</div>
        </div>
      </div>

      <router-view/>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import api from '@/api';

export default {
  name: 'app',
  computed: {
    ...mapState({
      alert: state => state.alert,
      account: state => state.account,
    }),
  },
  methods: {
    ...mapActions({
      clearAlert: 'alert/clear',
      logout: 'account/logout',
    }),
    newGame() {
      api.game.createGame()
        .then((game) => {
          this.$router.push({ name: 'Game', params: { id: game.id } });
        });
    },
  },
  watch: {
    $route() {
      this.clearAlert();
    },
  },
};
</script>

<style scoped>
#nav {
  padding-top: 5px;
  padding-left: 5px;
}
</style>
