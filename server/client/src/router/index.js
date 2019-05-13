import Vue from 'vue';
import Router from 'vue-router';
//import HelloWorld from '@/components/HelloWorld';
import Ping from '@/components/Ping';
import Orders from '@/components/Orders';
import NotFound from '@/components/NotFound';
import Login from '@/components/Login';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: {
        name: 'login',
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/secure',
      name: 'secure',
      component: Orders,
      props: true,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    // {
    //   path: '*',
    //   name: 'NotFound',
    //   component: 'NotFound',
    // },
  ],
  mode: 'history',
});
