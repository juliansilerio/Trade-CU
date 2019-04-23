import Vue from 'vue';
import Router from 'vue-router';
//import HelloWorld from '@/components/HelloWorld';
import Ping from '@/components/Ping';
import Orders from '@/components/Orders';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Orders',
      component: Orders,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
  mode: 'history',
});
