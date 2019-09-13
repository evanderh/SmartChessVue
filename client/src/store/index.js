import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';

import account from './account.module';
import alert from './alert.module';

Vue.use(Vuex);

const game = {
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
};

export default new Vuex.Store({
  modules: {
    account,
    alert,
    game,
  },
});
