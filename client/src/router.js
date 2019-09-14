import Vue from 'vue';
import Router from 'vue-router';

import Analysis from './views/Analysis.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Analysis,
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import(/* webpackChunkName: "about" */ './views/Login.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import(/* webpackChunkName: "about" */ './views/Register.vue'),
    },
    {
      path: '/game/:id',
      name: 'Game',
      component: () => import(/* webpackChunkName: "about" */ './views/Game.vue'),
    },
  ],
});
