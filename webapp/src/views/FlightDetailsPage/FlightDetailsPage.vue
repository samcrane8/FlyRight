<template>
  <div>
    <v-content style="margin-top:80px;margin-left:10px;margin-right:10px">
      <span style="font-size:30px;font-weight:200;margin-left:10px"> FLIGHT DETAILS </span>
      <span style="margin-top:-20px;"
      v-if="flight"> {{flight.title}} </span>
      <v-layout column>
        <v-layout row>
          <v-layout column
          style="width:50vw">
            <v-container fill-height>
              <v-layout row wrap align-center>
                <v-flex class="text-xs-center">
                  <map-thumbnail
                  :mission="flight"
                  v-if="flight"
                  width="45vw"
                  height="45vh"
                  :zoomControl="true"
                  :dragging="true"/>
                </v-flex>
              </v-layout>
            </v-container>
            <flight-details-info 
            xs4
            v-if="flight"
            :flight="flight"
            v-on:update_clearance="update_clearance"
            :is_gov_official="is_gov_official"
            :user_info="user_info"/>
          </v-layout>
          <flight-details-chat
          style="width:45vw"
          xs8
          :flight="flight"/>
        </v-layout>
      </v-layout>
      <flight-details-drones
      xs4
      :drones="drones"/>
    </v-content>
    <icarus-footer/>
  </div>
</template>

<script>
  import axios from 'axios'
  import VueAxios from 'vue-axios'
  import API from '@/mixins/API.js'
  import FlightDetailsInfo from './FlightDetailsInfo'
  import FlightDetailsChat from './FlightDetailsChat'
  import FlightDetailsDrones from './FlightDetailsDrones'
  import MapThumbnail from '@/components/MapThumbnail'
  import Footer from '@/components/Footer'

  export default {
    mixins: [API],
    components: {
      FlightDetailsInfo,
      FlightDetailsChat,
      FlightDetailsDrones,
      MapThumbnail,
      'icarus-footer': Footer,
    },
    data() {
      return {
        flight_id: '',
        flight: null,
        drones: null,
        user_info: null,
        is_gov_official: false,
      }
    },
    methods: {
      async get_added_drones() {
        var response = await this.get_mission_drones(
          this.flight.id,
          this.$store.state.access_token
        )
        return response.data
      },
      async fetch_mission_info() {
        const response = await this.get_mission_info(
          this.flight_id,
          this.$store.state.access_token
        );
        if (response.status == 200) {
          this.flight = response.data
          this.drones = await this.get_added_drones()
        }
      },
      async get_user(){
        var response = await this.get_current_user_info(this.$store.state.access_token);
        if (response.status == 200) {
          this.user_info = response.data
        }
      }, 
      async load_data() {
        this.flight_id = this.$route.query.id
        if (this.flight_id === 'null') {
          return
        }
        var response = await this.is_government_official(this.$store.state.access_token);
        if (response.data) {
          this.is_gov_official = true
        }
        await this.get_user();
        await this.fetch_mission_info();
      },
      async update_clearance(clearance) {
        const response = await this.edit_clearance(
					this.flight_id, clearance.state, clearance.message,
					this.$store.state.access_token
        );
        if (response.status == 200) {
          this.$emit('snackbar', 6000, 'Clearance updated.')
          this.load_data()
				}
      }
    },
    async mounted() {
      await this.load_data()
    },
    watch: {
      async '$route' (to, from) {
        // react to route changes...
        await this.load_data()
      }
    },
  }
</script>

<style>

</style>
