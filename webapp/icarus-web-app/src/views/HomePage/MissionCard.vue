<template>
  <div
	class="mission-card"
	width=250px
	@click="onClick">
		<map-thumbnail
		:mission="mission"
		width="250px"
		height="150px"
		style="width:250px;"
		/>
		<v-flex
			class="card-text"
		> 
			<span style="font-weight:500"> Title:</span> {{mission.title}} <br>
			<span style="font-weight:500"> Commander:</span> {{mission.commander_id}} <br>
			<span style="font-weight:500"> Starts at:</span> {{mission.starts_at | date_filter}} <br>
		</v-flex>
	</div>
</template>

<style>
	.mission-card {
		width:250px;
		height:250px;
	}
	.card-text {
		font-weight:300;
	}
</style>

<script>
import API from '@/mixins/API.js'
import router from '@/router'
import MapThumbnail from '@/components/MapThumbnail.vue'
import moment from 'moment'

export default {
	mixins: [API],
	props: ['mission'],
  components: {
    'map-thumbnail': MapThumbnail
  },
	data() {
		return {
		}
	},
	methods: {
    onClick(){
			router.push(`/flightdetails?id=${this.mission.id}`)
		}
	},
	filters: {
  	date_filter: function (date) {
    return moment(date).format('MMMM Do, YYYY');
  }
}

}
</script>
