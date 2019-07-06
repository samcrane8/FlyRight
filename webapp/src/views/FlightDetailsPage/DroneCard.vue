<template>
  <v-content>
    <v-layout row>
      <v-card
      style="
      height:150px;
      width:150px;">
        <img 
        v-if="drone.type=='Rotor'"
        width="150px" height="150px"
        src="/static/quadrotor_clipart.png"/>
        <img 
        v-if="drone.type=='Fixed-Wing'"
        width="150px" height="150px"
        src="/static/fixed_wing_clipart.jpg"/>
      </v-card>
      <v-layout column> 
        <div
        style="margin-left:8px;">
          <span style="font-weight:200;font-size:16px;">{{drone.name}}</span><br>
          {{drone.manufacturer}}<br>
          {{drone.faa_registration_number}}<br>
        </div>
      </v-layout>
    </v-layout>
  </v-content>
</template>

<script>
  export default {
    name: 'drone-card',
    props: ['drone']
  }
</script>

<style>

</style>
