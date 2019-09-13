import api from '../api';
import router from '../router';

const localUser = JSON.parse(localStorage.getItem('user'));
const initialState = localUser
  ? { status: { loggedIn: true }, user: localUser }
  : { status: {}, user: null };

export default {
  namespaced: true,
  state: initialState,
  actions: {
    login({ dispatch, commit }, { username, password }) {
      commit('loginRequest', { username });

      api.user.login(username, password)
        .then(
          (user) => {
            commit('loginSuccess', user);
            router.push('/');
          },
          (error) => {
            commit('loginFailure', error);
            dispatch('alert/error', error, { root: true });
          },
        );
    },
    logout({ commit }) {
      api.user.logout();
      commit('logout');
    },
    register({ dispatch, commit }, user) {
      commit('registerRequest');

      api.user.register(user)
        .then(
          () => {
            commit('registerSuccess');
            router.push('/login');
            setTimeout(() => {
              // display success message after route change completes
              dispatch('alert/success', 'Registration successful', { root: true });
            });
          },
          (error) => {
            commit('registerFailure', error);
            dispatch('alert/error', error, { root: true });
          },
        );
    },
  },

  mutations: {
    loginRequest(state, user) {
      state.status = { loggingIn: true };
      state.user = user;
    },
    loginSuccess(state, user) {
      state.status = { loggedIn: true };
      state.user = user;
    },
    loginFailure(state) {
      state.status = {};
      state.user = null;
    },
    logout(state) {
      state.status = {};
      state.user = null;
    },
    registerRequest(state) {
      state.status = { registering: true };
    },
    registerSuccess(state) {
      state.status = {};
    },
    registerFailure(state) {
      state.status = {};
    },
  },
};
