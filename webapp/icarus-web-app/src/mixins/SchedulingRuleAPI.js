//API JAVASCRIPT MIXIN

// define a mixin object
import Vue from 'vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
import qs from 'qs';
import * as data from '@/config/env.js'


Vue.use(VueAxios, axios)

export default {
  data () {
  	return data.default
  },
  methods: {
    async register_scheduling_rule(token, scheduling_rule) {
      var url = this.base_url + '/scheduling_rule/register/'
      return await axios.post(url, scheduling_rule, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async get_scheduling_rule(token, flight_id) {
      var url = this.base_url + '/scheduling_rule/get/?id=' + flight_id
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async edit_scheduling_rule(token, scheduling_rule) {
      var url = this.base_url + '/scheduling_rule/edit/'
      return await axios.post(url, scheduling_rule, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async delete_scheduling_rule(token, flight_id) {
      var url = this.base_url + '/scheduling_rule/delete/?id=' + flight_id
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
  }
}
