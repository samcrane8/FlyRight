<template>
  <v-content>
    <v-layout row>
      <jurisdiction-map v-if="department_info" :jurisdiction="department_info"/>
      <dashboard-stats v-if="department_info" :department_id="department_id" :department_name="department_name"
      v-on:snackbar="_snackbar"/>
    </v-layout>
  </v-content>
</template>


<script>
  import JurisdictionMap from './JurisdictionMap'
  import DashboardStats from './DashboardStats'
  import API from '@/mixins/API'

  export default {
    components: {
      'jurisdiction-map': JurisdictionMap,
      'dashboard-stats': DashboardStats
    },
    mixins: [API],
    data() {
      return {
        user_info: null,
        department_id: null,
        department_info: null,
        department_name: ""
      }
    },
    async mounted() {
      const response = await this.get_current_user_info(
        this.$store.state.access_token
      );
      this.user_info = response.data
    },
    methods: {
			_snackbar(timeout,text) {
				this.$emit('snackbar', timeout, text)
      },
      async load_data() {
        this.department_id = parseInt(this.$route.query.id)
        if (this.department_id === 'null') {
          return
        }
        var response = await this.get_department_info(this.$store.state.access_token,
        this.department_id);
        console.log(JSON.stringify(response.data))
        if (response.status == 200){
          this.department_info = response.data
          this.department_name = this.department_info.name
        }
      },
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
