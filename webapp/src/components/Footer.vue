<template>
  <span style="background-color:white;">
    <section style="margin-bottom:20px;margin-top:20px;">
      <v-layout row>
        <v-layout column style="margin-left:50px;">
          <v-flex class="text-xs-left"
          style="line-height:2;font-weight:300;">
            <span style="line-height:3;font-weight:400"> SERVICES<br> </span>
            <span style="cursor:pointer;" @click="goto('/privacy')"> Privacy </span><br>
          </v-flex>
        </v-layout>
        <!-- <v-flex class="text-xs-left"
        style="line-height:2;font-weight:300;">
          <span style="line-height:3;font-weight:400"> HELP<br> </span>
          <span style="cursor:pointer" @click="goto('/contact')"> Contact </span><br>
          <span style="cursor:pointer" @click="goto('/about')"> About </span><br>
        </v-flex> -->
      </v-layout>
    </section>
    <v-footer class="pa-3" style="background-color:white;">
      <v-spacer></v-spacer>
      <div>&copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
  </span>
</template>

<script>
  import router from '@/router'

  export default {
    name: 'icarus-footer',
    methods: {
      goto(loc){
        router.push(loc)
      }
    },
  }
</script>

<style>

</style>
