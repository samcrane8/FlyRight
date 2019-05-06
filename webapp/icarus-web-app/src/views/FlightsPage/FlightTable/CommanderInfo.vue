<template>
  <v-card flat>
    <v-card-text>
      <b>Name: </b> {{this.commander.user.first_name + ' ' + this.commander.user.last_name}} <br/>
      <b>Commander ID:</b> {{this.commander_name}}<br/>
      <b>Remote Pilot Certificate Number: </b> {{this.commander.pilot.remote_pilot_certificate_number}}<br/>
      <b>Mobile Phone Number:</b> {{this.commander.pilot.mobile_phone_number}}<br/>
    </v-card-text>
  </v-card>
</template>

<script>
  import API from '@/mixins/API'
  export default {
    mixins: [API],
    name: 'commander-info',
    props: ['created_by', 'commander_name'],
    data () {
      return {
        commander: {},
        user: {}
      }
    },
    methods: {
      
    },
    async mounted() {
      const response = await this.get_user_info(
        this.$store.state.access_token,
        this.created_by
      );
      this.commander = response.data
    }
  }
</script>