<template>
  <div class="container" id="app">
    <b-navbar id="nav" toggleable="lg" type="dark" variant="info">
        <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown v-if="authenticated" right>
          <!-- Using 'button-content' slot -->
          <template slot="button-content"><em>USER</em></template>
          <b-dropdown-item to="/login" v-on:click.native="logout()" replace>Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <router-view @authenticated="setAuthenticated" />
  </div>
</template>

<script>
export default {
  name: 'App',
  props: ['user'],
  data() {
    return {
      authentiated: false,
      user: {},
    }
  },
  mounted() {
    if(!this.authenticated) {
      this.$router.replace({ name:"login"});
    }
  },
  methods: {
    setAuthenticated(status) {
      this.authenticated = status;
    },
    logout() {
      this.authenticated = false;
    }
  }
};
</script>

<style>
#app {
  margin-top: 60px
}
</style>
