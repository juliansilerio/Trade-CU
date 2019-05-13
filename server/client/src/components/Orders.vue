<template>
<div class='container'>
  <b-alert v-model="showBadOrderAlert" variant="danger" dismissible>
     {{ orderMessage }}
   </b-alert>
   <b-alert v-model="showGoodAlert" variant="success" dismissible>
     {{ orderMessage }}
   </b-alert>
    <h1 class='text-center'>Trade@CU</h1>

    <b-navbar id='nav' toggleable='lg' type='dark' variant='dark'>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id='nav-collapse' is-nav>
      <b-navbar-nav>
        <b-navbar-brand>{{ this.user.uni }}</b-navbar-brand>
        <b-nav-item>Credits: {{ this.user.credits }}</b-nav-item>
        <button type='button' class='btn btn-success btn-sm' v-b-modal.order-modal>New Order</button>
      </b-navbar-nav>
    </b-collapse>
      <button type='button' class='btn btn-light btn-sm' to='/login' v-on:click='logout()' right>Sign Out</button>
    </b-navbar>
    <div class='container border mt-2'>
      <b-tabs pills variant='info' type='info'>
        <b-tab title="My orders">
          <table class='table'>
            <thead>
              <tr>
                <th style='width: 5%'>SIDE</th>
                <th style='width: 20%'>TICKER</th>
                <th>CLASS</th>
                <th style='width: 10%'>TIME</th>
                <th style='width: 10%'>PROFESSOR</th>
                <th style='width: 10%'>PRICE</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for='(order, index) in myOrders' :key='index'>
                <td v-if='order.side=="BUY"' class='bg-info'>
                  <h6 class='text-center'>BUY</h6>
                </td>
                <td v-else class='bg-warning'>
                  <h6 class='text-center'>SELL</h6>
                </td>
                <td>{{ order.ticker }}</td>
                <td>{{ order.class }}</td>
                <td>{{ order.time }}</td>
                <td>{{ order.professor }}</td>
                <td>{{ order.price }}</td>
                <td>
                  <button v-on:click='deleteOrder(order.id)' type='button' class='btn btn-danger btn-sm'>DELETE</button>
                </td>
              </tr>
            </tbody>
          </table>
        </b-tab>
        <b-tab title="Everyone else's orders">
          <table class='table'>
            <thead>
              <tr>
                <th style='width: 5%'>SIDE</th>
                <th style='width: 20%'>TICKER</th>
                <th>CLASS</th>
                <th style='width: 10%'>TIME</th>
                <th style='width: 10%'>PROFESSOR</th>
                <th style='width: 10%'>PRICE</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for='(order, index) in orders' :key='index'>
                <td v-if='order.side=="BUY"' class='bg-info'>
                    <h6 class='text-center'>BUY</h6>
                </td>
                <td v-else class='bg-warning'>
                    <h6 class='text-center'>SELL</h6>
                </td>
                <td>{{ order.ticker }}</td>
                <td>{{ order.class }}</td>
                <td>{{ order.time }}</td>
                <td>{{ order.professor }}</td>
                <td>{{ order.price }}</td>
                <td>
                  <button v-on:click='executeOrder(order.id)' type='button' class='btn btn-success btn-sm'>EXECUTE</button>
                </td>
              </tr>
            </tbody>
          </table>
        </b-tab>
      </b-tabs>
    </div>
    <b-modal ref='addOrderModal'
             id='order-modal'
             title='Add a new order'
             hide-footer>
      <b-form @submit='onSubmit' @reset='onReset' class='w-100'>
        <b-form-group id='form-course-group'
                    label='Course:'
                    label-for='form-course-input'>
          <b-form-select id='form-course-input'
                    v-model='addOrderForm.course'
                    :options='this.options' required>
            </b-form-select>
        </b-form-group>
        <b-form-group id='form-price-group'
                      label='price:'
                      label-for='form-price-input'>
          <b-form-input id='form-price-input'
                          type='number'
                          v-model='addOrderForm.price'
                          required
                          placeholder='Enter price'>
          </b-form-input>
        </b-form-group>
        <b-form-group label='BUY/SELL'>
          <b-form-radio v-model='addOrderForm.side' name='some-radios' value='BUY'>BUY</b-form-radio>
          <b-form-radio v-model='addOrderForm.side' name='some-radios' value='SELL'>SELL</b-form-radio>
        </b-form-group>
        <b-button type='submit' variant='primary'>Submit</b-button>
        <b-button type='reset' variant='danger'>Reset</b-button>
      </b-form>
    </b-modal>

    <router-view @user='getUser' />
</div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['user'],
  data() {
    return {
      showBadOrderAlert: 0,
      showGoodAlert: 0,
      orderMessage: '',
      orders: [],
      myOrders: [],
      addOrderForm: {
          course: '',
          price: '',
          side: '',
          user: '',
      },
      user: {
        uni: '',
        credits: 0,
      },
      options: [],
    };
  },
  methods: {
    getCourses() {
      const path = 'http://localhost:5000/courses';
      axios.get(path)
        .then((res) => {
          //console.log(res.data.courses)
          this.options = res.data.courses;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getOrders() {
      const path = 'http://localhost:5000/getOrders';
      const payload = { user: this.user}
      axios.post(path, payload)
        .then((res) => {
          this.orders = res.data.orders;
          this.myOrders = res.data.myOrders;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addOrder(payload) {
      const path = 'http://localhost:5000/addOrder';
      axios.post(path, payload)
        .then((res) => {
          this.getOrders();
          this.showBadOrderAlert = !res.data.executed;
          this.showGoodAlert = res.data.executed;
          this.orderMessage = res.data.message;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getOrders();
        });
    },
    initForm() {
      this.addOrderForm.course = '';
      this.addOrderForm.side = '';
      this.addOrderForm.price = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addOrderModal.hide();
      const payload = {
          course : this.addOrderForm.course,
          side: this.addOrderForm.side,
          price: this.addOrderForm.price,
          user: this.user,
      };
      this.addOrder(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addOrderModal.hide();
      this.initForm();
    },
    executeOrder(value) {
        const path='http://localhost:5000/execute';
        const payload = { order: value , user: this.user };
        axios.put(path, payload)
        .then((res) => {
          console.log(res.data.message);
          console.log(res.data);
          this.refresh();
          this.showBadOrderAlert = !res.data.executed;
          this.showGoodAlert = res.data.executed;
          this.orderMessage = res.data.message;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    deleteOrder(value) {
        const path='http://localhost:5000/delete';
        const payload = { order: value , user: this.user };
        axios.put(path, payload)
        .then((res) => {
          this.refresh();
          this.showBadOrderAlert = !res.data.executed;
          this.showGoodAlert = res.data.executed;
          this.orderMessage = res.data.message;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getUser() {
      const path = 'http://localhost:5000/user';
      // console.log(this.user);
      // console.log(this.props);
      // console.log(this.params);
      const payload = { user : this.user.uni };
      //const payload = { user : this.user };
      //console.log(this.data.user);
      // console.log(payload);
      axios.post(path, payload)
      .then((res) => {
        this.user = res.data.user;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
    },
    refresh() {
        this.getUser();
        this.getOrders();
        this.getCourses();
    },
    logout() {
      console.log('logging out');

      this.authenticated = false;
      this.user = '';
      this.$router.replace({name:'login'})
    }
  },
  created() {
      // refresh every 5 seconds
    this.refresh();
    this.interval = setInterval(() => this.refresh(), 5000);
    // console.log('test print 1');
    // console.log(this.$parent);
    // console.log(user);
    // console.log('test print 2');
  },
};
</script>
