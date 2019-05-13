<template>
  <div class='container' id='app'>
    <b-navbar v-if='authenticated'  id='nav' toggleable='lg' type='dark' variant='dark'>


        <b-navbar-nav >
          <b-nav-text right>{{ this.user.credits }}</b-nav-text>
          <b-nav-text right><em>{{ this.user.uni }}</em></b-nav-text>
          <b-nav-item to='/login' v-on:click.native='logout()' replace>Sign Out</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <router-view @status='setAuthenticated' />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      authenticated: false,
      user: '',
    }
  },
  mounted() {
    if(!this.authenticated) {
      this.$router.replace({ name:'login'});
    }
  },
  methods: {
    setAuthenticated(status) {
      console.log(status);
      this.authenticated = status.authenticated;
      this.user = status.user;
      //console.log(status.user)
      this.$router.replace({ name: 'secure',  params: {user: status.user }});
    },
    logout() {
      this.authenticated = false;
      this.user = '';
    },
  }
};
</script>

<style>
#app {
  margin-top: 60px
}
</style>
