<template>
  <v-card
  style="padding:10px;margin:10px;">
    <span style="font-size:25px;font-weight:200;"> CHAT </span>
    <v-container fill-height>
      <v-layout row wrap align-center>
          <v-flex class="text-xs-center"
          style="font-size:18px;">
            Chat is currently under construction. Hold tight, we are working hard to improve your experience!
            <br/> <br/>
            <v-flex> <v-icon>computer</v-icon></v-flex>
          </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
export default {
  name:'flight-details-chat',
  props: {
    flight: {
      type: Object,
      default() {
        return { message: 'hello' }
      }
    }
  }
}
</script>

<style>

</style>
