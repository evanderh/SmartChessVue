import Vue from 'vue';
import Vuex from 'vuex';

import api from './api';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userID: null,
    startFEN: '',
  },
  mutations: {
    loadGame(state, id) {
      return api.loadGame(id)
        .then(response => state.commit('setGame', response));
    },
  },
  actions: {
    setGame(state, payload) {
      if (payload) {
        state.boardID = payload.id;
        state.startFEN = payload.fen;
      }
    },
  },
});
