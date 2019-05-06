<template>
  <div>
    <div style="margin-top:15vh;
    margin-left:5vh;margin-right:5vh;">
      <v-layout column>
        <mission-carousel
          :missions="current_missions"
          title="CURRENT FLIGHTS"
        />
        <mission-carousel
          :missions="past_missions"
          title="RECENT FLIGHTS"
        />
        <mission-carousel
          :missions="upcoming_missions"
          title="UPCOMING FLIGHTS"
        />
      </v-layout>
    </div>
    <icarus-footer/>
  </div>
</template>



<script>
import Vue from 'vue';
import router from '@/router'
import API from '@/mixins/API.js'
import MissionCarousel from './MissionCarousel'
import Footer from '@/components/Footer'

export default {
  name: 'Login',
  mixins: [API],
  components: {
    'mission-carousel': MissionCarousel,
    'icarus-footer': Footer
  },
  data () {
    return {
      past_missions: [],
      current_missions: [],
      upcoming_missions: []
    }
  },
  methods: {
    
  },
  async mounted() {
    var response = await this.get_past_missions(
      this.$store.state.access_token
    );
    this.past_missions = response.data

    response = await this.get_current_missions(
      this.$store.state.access_token
    );
    this.current_missions = response.data

    response = await this.get_upcoming_missions(
      this.$store.state.access_token
    );
    this.upcoming_missions = response.data
  }
}
</script>


<style>
.rowHeader {
  font-weight:200;
  font-size:24px;
}
</style>