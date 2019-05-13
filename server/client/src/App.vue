<template>
  <div class='container' id='app'>
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
    };
  },
  mounted() {
    if (!this.authenticated) {
      this.$router.replace({ name: 'login' });
    }
  },
  methods: {
    setAuthenticated(status) {
      if (status.authenticated) {
        console.log(status);
        this.authenticated = status.authenticated;
        this.user = status.user;
        //console.log(status.user)
        this.$router.replace({ name: 'secure', params: { user: status.user } });
      }
    },
    logout() {
      console.log('logging out');
      this.authenticated = false;
      this.user = '';
    },
  },
};
</script>

<style>
#app {
  margin-top: 60px
}
</style>
