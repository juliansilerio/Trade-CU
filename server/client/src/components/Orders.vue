<template>
<div class="container">
    <h1 class="text-center">Trade@CU</h1>
    <button type="button" class="btn btn-success btn-sm" v-b-modal.order-modal>New Order</button>
    <!--div class="container">
        <form>
            <div class="form-group">
                <label for="class_lookup">Class ticket</label>
                <input type="text" class="form-control" id="class_lookup"  placeholder="Look up a class">
            </div>
        </form>
        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <button type="button" class="btn btn-primary">BUY</button>
            </div>
            <input type="text" class="form-control" placeholder="Price">
            <div class="input-group-append">
                <button type="button" class="btn btn-secondary border-white border-top-0 border-bottom-0">BID</button>
                <button type="button" class="btn btn-secondary border-white border-top-0 border-bottom-0">ASK</button>
                <button type="button" class="btn btn-secondary border-white border-top-0 border-bottom-0">LAST</button>
                <button type="button" class="btn btn-success">EXECUTE</button>
            </div>
        </div>
    </div-->
    <div class="container border mt-2">
        <table class="table">
            <thead>
                <tr>
                    <th style="width: 5%">SIDE</th>
                    <th style="width: 20%">TICKER</th>
                    <th>CLASS</th>
                    <th style="width: 10%">TIME</th>
                    <th style="width: 10%">PROFESSOR</th>
                    <th style="width: 10%">PRICE</th>
                    <th>ACTIONS</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(order, index) in orders" :key="index">
                    <td v-if="order.side=='BUY'" class="bg-info">
                        <h6 class="text-center">BUY</h6>
                    </td>
                    <td v-else class="bg-warning">
                        <h6 class="text-center">SELL</h6>
                    </td>
                    <td>{{ order.ticker }}</td>
                    <td>{{ order.class }}</td>
                    <td>{{ order.time }}</td>
                    <td>{{ order.professor }}</td>
                    <td>{{ order.price }}</td>
                    <td>
                        <button type="button" class="btn btn-success btn-sm">EXECUTE</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <b-modal ref="addOrderModal"
             id="order-modal"
             title="Add a new order"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-class-group"
                    label="Class:"
                    label-for="form-class-input">
          <b-form-input id="form-class-input"
                        type="text"
                        v-model="addOrderForm.class"
                        required
                        placeholder="Enter class">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-professor-group"
                      label="Professor:"
                      label-for="form-professor-input">
            <b-form-input id="form-professor-input"
                          type="text"
                          v-model="addOrderForm.professor"
                          required
                          placeholder="Enter professor">
            </b-form-input>
          </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <router-view @user="getUser" />
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: [],
      addOrderForm : {
          class : '',
          professor : '',
      },
      user: {
        uni : '',
        credits : 0,
      },
    };
  },
  methods: {
    getOrders() {
      const path = 'http://localhost:5000/orders';
      axios.get(path)
        .then((res) => {
          this.orders = res.data.orders;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addOrder(payload) {
      const path = 'http://localhost:5000/orders';
      axios.post(path, payload)
        .then(() => {
          this.getOrders();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getOrders();
        });
    },
    initForm() {
      this.addOrderForm.class = '';
      this.addOrderForm.professor = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addOrderModal.hide();
      const payload = {
        class: this.addOrderForm.class,
        professor: this.addOrderForm.professor,
      };
      this.addOrder(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addOrderModal.hide();
      this.initForm();
    },
    getUser() {
      const path = "http://localhost:5000/user";
      const payload = { user: "jjs2245" };
      console.log(payload)
      axios.post(path, payload)
      .then((res) => {
        //console.log(res.data.user);
        this.user = res.data.user;
        //console.log(this.user.credits);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
    },
  },
  created() {
    //console.log(this.user);
    this.getUser();
    this.getOrders();
  },
};
</script>
