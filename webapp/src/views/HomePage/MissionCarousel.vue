<template>
  <v-layout column>
		<v-flex>
			<h1 class="rowHeader"> {{title}} </h1>
		</v-flex>
		<v-layout row
        style="
        margin-left:25px;
        margin-top:15px;
				margin-bottom:15px;
        overflow-x:scroll;
        ">
			<v-flex
			v-if="missions && missions.length > 0"
      v-model="missions" 
      v-for="mission in missions" 
		  :key="mission.id"
      style="margin-right:15px;">
				<mission-card
        :mission="mission"
				zoomControl="false"
        />
			</v-flex>
			<v-flex
			v-if="missions.length == 0"
			class="text-xs-center"
			>
			CURRENTLY NO MISSIONS TO DISPLAY
			</v-flex>
		</v-layout>
	</v-layout>
</template>

<style>

</style>

<script>
import API from '@/mixins/API.js'
import router from '@/router'
import MissionCard from './MissionCard'

export default {
	mixins: [API],
	props: ['missions', 'title'],
  components: {
    'mission-card': MissionCard
  },
	data() {
		return {
		}
	},
	methods: {
    
	}
}
</script>
