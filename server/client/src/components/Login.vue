<template>
  <div>
  <div class='container mb-2' id='login'>
    <h1><Login</h1>
    <input type='text' name='username' v-model='input.username' placeholder='Username' />
    <button class='btn btn-info' type='button' v-on:click='login()'>Login</button>
  </div>
    <b-alert v-model='bad_login' variant='danger' dismissible>
    {{ this.badLoginMsg }}
    </b-alert>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      bad_login: false,
      badLoginMsg: '',
      input: {
        username: '',
      },
    };
  },
  methods: {
    login() {
      const path = 'http://localhost:5000/check_user';
      if (this.input.username !== '') {
        const payload = {
          username: this.input.username,
        };
        axios.post(path, payload)
          .then((response) => {
            if (response.data.authenticated) {
              this.$emit('status', response.data);
            } else {
              this.badLoginMsg = 'Username not found';
              this.bad_login = true;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        this.badLoginMsg = 'Username can\'t be empty';
        this.bad_login = true;
      }
    },
  },
};
</script>
