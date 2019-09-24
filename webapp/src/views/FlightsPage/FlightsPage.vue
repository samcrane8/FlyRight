<template>
	<v-content class="mission_body">
		<v-layout row style="margin-top:70px;">
			<v-flex xs5>
				<v-layout column>
					<filters-card
          @afterchange="afterFilterHandler"
          @beforechange="beforeFilterHandler"
          @refresh_missions="getMissions"
          />
					<v-card style="margin-left:20px;margin-right:20px;">
						<v-flex class="text-xs-center">
							<v-btn flat outline style="margin:10px;"
								@click="newMission()">
								NEW FLIGHT PLAN
							</v-btn>
						</v-flex>
					</v-card>
					<v-card style="margin-left:20px;margin-right:20px;">
						<v-flex class="text-xs-center">
							<v-btn flat outline style="margin:10px;" @click="viewCalendar()">
								<v-icon>
									event
								</v-icon>
								View Calendar
							</v-btn>
						</v-flex>
					</v-card>
				</v-layout>
			</v-flex>
			<flights-table
      :missions="missions"
      :user_info="user_info"
	  :department_name="department_name"
      :is_gov_official="is_gov_official"
      @delete_mission="deleteMission"
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
  
  import FiltersCard from './FlightFilters/FiltersCard'
	import FlightsTable from './FlightTable//FlightsTable'
	import Footer from '@/components/Footer'

	export default {
		name: 'MissionsPage',
		mixins: [API],
		user_info: null,
		components: {
      'filters-card': FiltersCard,
			'flights-table': FlightsTable,
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
        if (this.afterFilter !== '') {
          filters.push({title:'after', datetime:this.afterFilter})
        }
        if (this.beforeFilter !== '') {
          filters.push({title:'before', datetime:this.beforeFilter})
        }
				var response = await this.post_get_missions(
          filters,
					this.$store.state.access_token
				);
				this.missions = response.data
      },
			async deleteMission(mission) {
				const response = await this.delete_mission(mission,
					this.$store.state.access_token
				);
				if (response.status == 200) {
					this.$emit('snackbar', 6000, 'Flight Deleted.')
					this.getMissions()
				}
				this.showDeleteWarning=false;
			},
			newMission(){
			  router.push('/newflight')
      },
	  viewCalendar() {
			router.push('./calendar')
		},
      afterFilterHandler(value) {
        this.afterFilter = value
      },
      		beforeFilterHandler(value) {
        	this.beforeFilter = value
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
		},
		filters: {
  		date_filter: function (date) {
    		return moment(date).format('MMMM Do, YYYY');
			},
			datetime_filter: function (date) {
    		return moment(date).format('MMMM Do YYYY, h:mm a');
			}
		}
	}
</script>
