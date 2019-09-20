<template>
    <v-content class="mission_body">
        <v-layout row style="margin-top:70px;">
            <calendar
                :missions="missions"
                :user_info="user_info"
                :department_name="department_name"
                :is_gov_official="is_gov_official"
                @snackbar='snackbar'
            />
        </v-layout>
        <icarus-footer/>
    </v-content>
</template>

<style>
    @import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500');

    .mission_body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f0f0;
    }
</style>


<script>
    import Vue from 'vue';
    import Vuetify from 'vuetify'
    import router from '@/router'
    import API from '@/mixins/API.js'
    import moment from 'moment'
    import Calendar from './Calendar'
    import Footer from '@/components/Footer'
    
    Vue.use(Vuetify)

    export default {
        name: 'CalendarPage',
        mixins: [API],
        user_info: null,
        components: {
            // 'filters-card': FiltersCard,
            'calendar': Calendar,
            'icarus-footer': Footer,
        },
        data () {
            return {
          afterFilter: '',
          beforeFilter: '',
          missions: [],
          user_info: null,
          is_gov_official: false,
          department_info: null,
          department_name: ""
        }
      },
        methods: {
            async getMissions() {
                var filters = []
                var response = await this.get_missions(
                    this.$store.state.access_token
                );
                this.missions = response.data
            },
            snackbar(time, message) {
                this.$emit('snackbar', time, message)
            },
            async load_data() {
                var response = await this.get_user_departments(this.$store.state.access_token);
                if (response.status == 200){
                    this.department_info = response.data
                    this.department_name = this.department_info[0].name;
                    this.department_info = this.department_info[0]
                }
            },
        },
        async mounted () {
            var response = await this.is_government_official(this.$store.state.access_token);
            if (JSON.stringify(response.data) == 'true') {
                this.is_gov_official = true
            }
            await this.getMissions();
            response = await this.get_current_user_info(this.$store.state.access_token);
            if (response.status == 200) {
                this.user_info = response.data
            }
            await this.load_data();

        },
            watch: {
            async '$route' (to, from) {
                // react to route changes...
                await this.load_data()
            }
        }
    }
</script>