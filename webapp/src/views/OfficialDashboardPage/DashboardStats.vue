<template>
  <v-content>
    <v-layout column
    class="stats_page"
    style="
      width:45vw;"
      >
      <v-flex class="text-xs-left"
      style="
      margin:15px;">
        <div class="stat_header">
          {{department_name}}
        </div>
        <v-card style="padding:10px;">
          <v-flex>
            <v-select
              :items="timeframes"
              v-model="curr_timeframe"
              label="Set Timeframe"
              single-line
              bottom
              style="width:10vw"
              @change="update_histogram"
            ></v-select>
          </v-flex>
          <div style="margin:5px;">
            <flight-histogram
            :chartData="data_collection"
            v-if="data_collection"
            :options="{responsive:false}"
            :width="400"
            :height="150"
            style="overflow:scroll;"
            />
          </div>
        </v-card>
      </v-flex>
      <v-flex style="margin:15px">
        <message-jurisdiction
        :department_name="department_name"
        v-on:snackbar="_snackbar"/>
      </v-flex>
    </v-layout>
  </v-content>
</template>

<script>
  import FlightHistogram from './DashboardGraphs/FlightHistogram'
  import MessageJurisdiction from './MessageJurisdiction'
  import API from '@/mixins/API'
  import moment from 'moment'

  export default {
    props: ['department_id', 'department_name'],
    mixins: [API],
    components: {
      'flight-histogram': FlightHistogram,
      'message-jurisdiction': MessageJurisdiction
    },
    data () {
      return {
        data_collection: null,
        timeframes: ['Week', 'Month', 'Year'],
        curr_timeframe: 'Week'
      }
    },
    methods: {
      _snackbar(timeout,text) {
				this.$emit('snackbar', timeout, text)
      },
      get_data_collection(data, labels, label) {
        this.data_collection = {
          labels,
          datasets: [
            {
              label,
              backgroundColor: null,
              data
            }
          ]
        }
      },
      async last_weeks_flights() {
        var today = moment().startOf('day')
        var one_week_ago = moment().startOf('day')
        one_week_ago.subtract(7, 'days');
        const response = await this.flight_histogram(
          this.department_id,
          one_week_ago.toISOString(), today.toISOString(),
          this.$store.state.access_token
        )
        if (response.status == 200) {
          var data = response.data
          console.log(JSON.stringify(data))
          var labels = Array.apply(null, Array(data.length)).map(function (_, i) {
              return one_week_ago.add(1, 'days').format('ddd');
          });
          this.get_data_collection(data, labels, 'Last Week Flights')
        }
      },
      async last_month_flights() {
        var today = moment().startOf('day')
        var one_month_ago = moment().startOf('day')
        one_month_ago.subtract(1, 'month');
        const response = await this.flight_histogram(
          this.department_id,
          one_month_ago.toISOString(), today.toISOString(),
          this.$store.state.access_token
        )
        if (response.status == 200) {
          var data = response.data
          var labels = Array.apply(null, Array(data.length)).map(function (_, i) {
              return one_month_ago.add(1, 'days').format('MM/DD');
          });
          this.get_data_collection(data, labels, 'Last Month Flights')
        }
      },
      async last_year_flights() {
        var today = moment().startOf('day')
        var one_year_ago = moment().startOf('day')
        one_year_ago.subtract(1, 'year');
        const response = await this.flight_histogram(
          this.department_id,
          one_year_ago.toISOString(), today.toISOString(),
          this.$store.state.access_token
        )
        if (response.status == 200) {
          var data = response.data
          var labels = Array.apply(null, Array(data.length)).map(function (_, i) {
              return one_year_ago.add(1, 'days').format('MM/DD');
          });
          this.get_data_collection(data, labels, 'Last year Flights')
        }
      },
      async update_histogram(value) {
        if (value == 'Week') {
          await this.last_weeks_flights();
        } else if (value == 'Month') {
          await this.last_month_flights();
        } else if (value == 'Year') {
          await this.last_year_flights();
        }
      }
    },
    async mounted() {
      await this.last_weeks_flights()
    }
  }
</script>

<style>
  .stats_page {
    height:100vh;
    overflow:scroll;
    padding-top:70px;
  }

  .stat_header {
    font-weight:200;
    font-size:25px;
    padding-bottom: 10px;
  }
</style>
