<template>
  <v-card dark class="light-green darken-4" style="height:400px;width:400px;">
    <v-card-media :src="require('@/assets/noMissionImage.png')" height="200px" style="margin-left:5%;margin-right:7.5%;">
    </v-card-media>
    <v-container fluid grid-list-lg>
      <v-layout row justify-left>
        <v-flex class="text-xs-center">
          <div>
            <div class="text-xs-center" style="font-size:25px;">  No Flights Available </div>
            <v-divider></v-divider>
            <v-flex class="text-xs-center">
              <v-btn v-on:click="newMission" class="light-green darken-2">New Flight</v-btn>
            </v-flex>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<style>

</style>

<script>
import router from '@/router'

export default {
	methods: {
    newMission() {
      router.push('/newflight')
    }
	}
}
</script>
