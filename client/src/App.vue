<template>
  <div id="app">
    <hr />

    <!-- <div id="nav">

      <router-link to="/">Smart Chess</router-link> |

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

      <button @click="playGame">Play</button>

    </div> -->

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
