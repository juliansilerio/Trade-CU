<template>
  <div class="container" id="app">
    <div id="nav">
        <router-link class="btn btn-danger float-right" v-if="authenticated" to="/login" v-on:click.native="logout()" replace>Logout</router-link>
    </div>
    <router-view @authenticated="setAuthenticated" />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      authentiated: false,
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
