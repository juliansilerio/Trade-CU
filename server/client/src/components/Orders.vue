<template>
<div class="container">
    <h1 class="text-center">Trade@CU</h1>
    <div class="container border">
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
    </div>
    <div class="container border">
        <table class="table">
            <thead>
                <tr>
                    <th style="width: 10%">SIDE</th>
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
                    <td>
                        <span v-if="order.side=='B'" class="bg-info">BUY</span>
                        <span v-else class="bg-warning">SELL</span>
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
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: [],
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
  },
  created() {
    this.getOrders();
  },
};
</script>
