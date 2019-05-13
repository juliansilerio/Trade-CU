<template>
  <div class='container' id='app'>
    <b-navbar id='nav' toggleable='lg' type='dark' variant='info'>
        <b-navbar-nav class='ml-auto'>
        <b-nav-item-dropdown v-if='authenticated' right>
          <!-- Using 'button-content' slot -->
          <template slot='button-content'><em>{{ this.user.uni }}</em></template>
          <b-dropdown-item to='/login' v-on:click.native='logout()' replace>Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
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
