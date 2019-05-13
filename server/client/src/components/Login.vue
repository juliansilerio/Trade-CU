<template>
  <div class='container' id='login'>
    <h1><Login</h1>
    <input type='text' name='username' v-model='input.username' placeholder='Username' />
    <button class='btn btn-info' type='button' v-on:click='login()'>Login</button>
    <!--p v-if='bad_login' id='warning'>
    That didn't work, please try again.
  </p-->
</div>
</template>

<script>
import axios from 'axios';

export default {
  name : 'Login',
  data() {
    return {
      input: {
        username: '',
      }
    }
  },
  methods: {
    login() {
      const path = 'http://localhost:5000/check_user'
      if(this.input.username != '') {
        const payload = {
          username: this.input.username,
        };
        axios.post(path, payload)
        .then(response => {
          if (response.data.authenticated) {
            this.$emit('status', response.data);
          } else {
            console.log('Username not found');
          }
        })
        .catch(error => {
          console.log(error)
        });

      } else {
        console.log('Username can\'t be empty');
      }
    }
  }
}
</script>
