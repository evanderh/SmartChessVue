<template>
  <div id="app">

    <div id="nav">

      <router-link to="/">BenderChess</router-link> |

      <router-link
        v-if="!account.status.loggedIn"
        to="/login">
        Login
      </router-link>
      <router-link
        v-else
        to="/login">
        Logout
      </router-link> |

      <button v-on:click="playGame">Play</button>

    </div>

    <div class="jumbotron">
      <div class="container">
        <div class="row">
          <div class="col-sm-6 offset-sm-3">
            <div v-if="alert.message" :class="`alert ${alert.type}`">{{alert.message}}</div>
            <router-view/>
          </div>

          <div
            v-if="account.status.loggedIn"
            class="col-sm-6 offset-sm-3">
            <p>{{ account.user.username }}</p>
          </div>
        </div>
      </div>
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
    playGame() {
      api.game.createGame()
        .then((gameID) => {
          this.$router.push({ name: 'Game', params: { id: gameID } });
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
