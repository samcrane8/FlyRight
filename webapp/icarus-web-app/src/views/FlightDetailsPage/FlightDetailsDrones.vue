<template>
  <v-card
  style="padding:10px;margin:10px;">
    <span style="font-size:25px;font-weight:200;margin-left:10px;"> DRONES </span>
    <v-layout row wrap>
      <v-flex
      v-for="(drone, index) in drones"
      :key="index"
      style="margin:20px;"
      >
        <drone-card :drone="drone" />
      </v-flex>
      <v-spacer/>
    </v-layout>
  </v-card>
</template>

<script>
  import DroneCard from './DroneCard'

  export default {
    name: 'flight-details-drones',
    components: {
      DroneCard
    },
    props: {
      drones: {
        type: Array,
        default() {
          return []
        }
      }
    }
  }
</script>

<style>

</style>
